from dataclasses import dataclass, field

@dataclass(order=True)
class MLData:
    first_buy_date: str
    last_buy_date: str
    second_last_buy_date: str
    third_last_buy_date: str
    # nft: str
    token_id: int
    n_txns: int
    n_unique_buyers: int
    fraudulent: str
    fraudulent_ascii: int
