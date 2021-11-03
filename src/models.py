from dataclasses import dataclass

@dataclass
class Bucket():
     name: str
     result: float
     lower: float
     upper: float

@dataclass
class BudgetStat():
     name: str
     value: float