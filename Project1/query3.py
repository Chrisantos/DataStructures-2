import pandas as pd 
import numpy as np
import glob
import time
from typing import Dict, List
from datetime import datetime
import matplotlib.pyplot as plt 

##################################################### Data ###################################################
from dataclasses import dataclass, field

@dataclass(order=True)
class Query3Data:
    buyer: str
    buyer_int: int
    n_txns: int

@dataclass(order=True)
class NFTTransaction:
    txn_hash: str
    time_stamp: str
    date_time: str
    action: str
    buyer: str
    buyer_int: int
    nft: str
    token_id: int
    type_: int
    quantity: int
    price: float
    price_str: str
    market: str
    n_unique_buyers: int

#################################################### Merge sort ##############################################
def merge_sort_by_ntxn(A: List[Query3Data]):
    if len(A) == 1:
        return A

    q = int(len(A)/2)
    B = A[:q]
    C = A[q:]

    L = merge_sort_by_ntxn(B)
    R = merge_sort_by_ntxn(C)
    return merge_by_ntxn(L, R)

def merge_by_ntxn(L: List[Query3Data], R: List[Query3Data]):
    n = len(L) + len(R)
    i = j = 0
    B = []
    for k in range(0, n):
        if j >= len(R) or (i < len(L) and L[i].n_txns >= R[j].n_txns):
            B.append(L[i])
            i = i + 1
        else:
            B.append(R[j])
            j = j + 1

    return B

#################################################### Radix sort ##############################################

def counting_sort_by_n_txns(A: List[Query3Data], exp) -> List[Query3Data]:
    n = len(A)
 
    # The output array elements that will have sorted arr
    output = [0] * (n)
 
    # initialize count array as 0
    count = [0] * (10)
 
    # Store count of occurrences in count[]
    for i in range(0, n):
        index = int(A[i].n_txns) // exp
        index = int(index)

        count[index % 10] += 1
 
    # Change count[i] so that count[i] now contains actual
    # position of this digit in output array
    for i in range(1, 10):
        count[i] += count[i - 1]
 
    # Build the output array
    i = n - 1
    while i >= 0:
        index = int(A[i].n_txns) // exp
        index = int(index)

        output[count[index % 10] - 1] = A[i]
        count[index % 10] -= 1
        i -= 1
 
    return output
 
# Method to do Radix Sort
def radix_sort_by_n_txns(A: List[Query3Data]) -> List[Query3Data]:
    # Find the maximum number to know number of digits
    max1 = max_by_n_txns(A)
 
    # Do counting sort for every digit. Note that instead
    # of passing digit number, exp is passed. exp is 10^i
    # where i is current digit number
    exp = 1
    while max1 / exp >= 1:
        A = counting_sort_by_n_txns(A, exp)
        exp *= 10

    B = []
    n = len(A)
    for i in range(n):
        B.append(A[n - i - 1])

    return B

def max_by_n_txns(A: List[Query3Data]) -> List[Query3Data]:
    max = 0
    for value in A:
        n_txns = int(value.n_txns)
        if  n_txns > max:
            max = n_txns

    return max

########################################## Utils #####################################################

def get_all_transactions(data: List[NFTTransaction]):
    hash = {}

    for row in data:
        if row.buyer_int in hash:
            hash[row.buyer_int].append(row)
        else:
            hash[row.buyer_int] = [row]

    return hash

def save_result(data: List[Query3Data], all_txns):
    all_txns = get_all_transactions(all_txns)

    with open("query3_out.txt", "w") as file:
        for row in data:
            file.writelines(f"{row.buyer} (frequency = {row.n_txns})\n")
            file.writelines("Buyer,\t Txn hash,\t Date Time (UTC),\t Buyer,\t NFT,\t Type,\t Quantity,\t Price (USD)\n")
            file.writelines("\n")
            for value in all_txns[row.buyer_int]:
                file.writelines(f"{value.buyer},\t {value.txn_hash},\t {value.date_time},\t {value.nft},\t {value.type_},\t {value.quantity},\t {value.price}\n")

            file.writelines("\n\n")

def currency_converter(data: List[NFTTransaction]) -> List[NFTTransaction]:
  for row in data:
    price = row.price_str

    if type(price) is not str:
      row.price = float(float(price) * 1.00)
      continue

    try:
      price, currency, _ = price.split(" ")
      price = price.replace(",", "")

      if currency == "ETH":
        row.price = float(float(price) * 1309.97)
      
      elif currency == "WETH":
        row.price = float(float(price) * 1322.16)

      elif currency == "ASH":
        row.price = float(float(price) * 0.9406)
      
      elif currency == "GALA":
        row.price = float(float(price) * 0.03748)
        
      elif currency == "TATR":
        row.price = float(float(price) * 0.012056)
        
      elif currency == "USDC":
        row.price = float(float(price) * 1.00)
        
      elif currency == "MANA":
        row.price = float(float(price) * 0.64205)
        
      elif currency == "SAND":
        row.price = float(float(price) * 0.7919)
        
      elif currency == "RARI":
        row.price = float(float(price) * 2.18)
        
      elif currency == "CTZN":
        row.price = float(float(price) * 0.00321)
        
      elif currency == "APE":
        row.price = float(float(price) * 4.62)

      else:
        row.price = float(float(price) * 1.00)

    except ValueError:
      None
      
  return data

def prepare_data(data) -> List[NFTTransaction]:
  data = data.reset_index()  # make sure indexes pair with number of rows

  transactions = []
  for i, row in data.iterrows():
    buyer_int = convert_string_to_ascii(row['Buyer'])

    transactions.append(NFTTransaction(
        txn_hash=row['Txn Hash'], 
        time_stamp=row['UnixTimestamp'],
        date_time=row['Date Time (UTC)'],
        action=row['Action'],
        buyer=row['Buyer'],
        buyer_int=buyer_int,
        nft=row['NFT'],
        token_id=row['Token ID'],
        type_=row['Type'],
        quantity=row['Quantity'],
        price_str=row['Price'],
        price=0.0,
        market=row['Market'],
        n_unique_buyers=0))
    
  return transactions

def get_dataframe(data: List[Query3Data]):
  txns_list = []

  for row in data:
    dic = {
        'Buyer': row.buyer,
        'Number of Transactions': row.n_txns,
    }
    txns_list.append(dic)

  df = pd.DataFrame.from_records(txns_list)
  df.to_excel('query3_out.xlsx') 
  return df

def update_with_n_txns(sorted_txns: List[NFTTransaction]) -> List[Query3Data]:
  # Lets sort the token ids by the number of unique buyers
  count = 0
  n = len(sorted_txns)

  new_txns = []
  
  for i, row in enumerate(sorted_txns):
      count += 1

      # This is for the scenario when the transaction is the last in the array (spreadsheet)
      if i == n - 1:
          data = Query3Data(buyer=sorted_txns[i].buyer, buyer_int=sorted_txns[i].buyer_int, n_txns=count)
          new_txns.append(data)

      elif sorted_txns[i].buyer_int != sorted_txns[i+1].buyer_int:
          data = Query3Data(buyer=sorted_txns[i].buyer, buyer_int=sorted_txns[i].buyer_int, n_txns=count)
          new_txns.append(data)

          count = 0

  return new_txns

def plot_graph(asymptotic_runtimes, actual_runtimes, filename="query_3.png", rows=92):
    x_axis = [i for i in range(rows)]
    plt.plot(x_axis, asymptotic_runtimes, color ='red')
    plt.plot(x_axis, actual_runtimes, color ='blue')
    plt.xlabel("Transaction Batch (x1000)")
    plt.ylabel("Runtime")
    plt.title("Runtime vs Transaction batch size")
    plt.legend(['Asymptotic Runtime (x5000)', 'Actual Runtime ((x10000))'], loc='upper left')

    plt.savefig(filename)

    plt.show()

def convert_string_to_ascii(input):
  a = list(input.encode('ascii'))
  return int("".join(map(str, a)))

############################################ Main Program ######################################################

def main():

    # please replace this with the path where the dataset file is
    files = glob.glob("/Users/chrisantuseze/VSCodeProjects/DataStructures 2/Project1/*.csv")

    data = [pd.read_csv(f) for f in files]
    data = pd.concat(data,ignore_index=True)
    data = data.dropna()

    transactions = prepare_data(data)
    transactions = currency_converter(transactions)

    elapsed_time_averages = []
    asymptotic_times = []

    rows = int(len(transactions)/1000)
    for i in range(rows):
        print(f"{(i + 1) * 1000} transactions")

        n = (i + 1) * 1000
        aveg_elapsed_time_ns = run_n_times(transactions[0: n], 100)
        elapsed_time_averages.append(aveg_elapsed_time_ns)

        # this is used to ensure both the asymptotic and actual run time have the same scale
        n *= 5000

        # we figured out that the token with the most number of transactions had 1209 transactions, hence the exponent, k = 4
        k = 3
        asymptotic_times.append(n * k)

    plot_graph(asymptotic_runtimes=asymptotic_times, actual_runtimes=elapsed_time_averages, rows=rows)

    # run_query(transactions, run=1)

def run_n_times(transactions, n):
    elapsed_times = []
    for i in range(n):
        elapsed_time, sorted_txns = run_query(transactions, run=i+1)
        elapsed_times.append(elapsed_time)

    aveg_elapsed_time_ns = sum(elapsed_times)/len(elapsed_times)
    aveg_elapsed_time_s = aveg_elapsed_time_ns/1e9
    print(f"\nThe average elapsed time is {aveg_elapsed_time_ns} nano secs (i.e {aveg_elapsed_time_s} secs)\n")

    return aveg_elapsed_time_ns

def run_query(transactions, run=1):
    data = process_data(transactions)

    start_time = time.time_ns()
    sorted_txns = radix_sort_by_n_txns(data)
    end_time = time.time_ns()

    elapsed_time = (end_time - start_time)

    if run == 1:
        save_result(sorted_txns, transactions)

        df = get_dataframe(sorted_txns)
        print(df.head(10))

        print(f"Run - {run} Sorting took {elapsed_time} nano secs ({elapsed_time/1e9} secs)")


    return elapsed_time, sorted_txns

def process_data(A: List[NFTTransaction]) -> List[Query3Data]:
    hash = {}
    for row in A:
        if row.buyer_int in hash:
            hash[row.buyer_int].append(row)
        else:
            hash[row.buyer_int] = [row]
        
    transactions = []
    for key in hash:
        transactions = np.concatenate((transactions, hash[key]))

    A = update_with_n_txns(transactions)
    return A

if __name__ == "__main__":
    main()