from dataclasses import dataclass, field

@dataclass(order=True)
class Query3Data:
    txn_hash: str
    token_id: int
    quantity: int
    price: str
    avg: float