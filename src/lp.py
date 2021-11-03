from typing import Dict, Tuple, List
import cvxpy as cp
import numpy as np
from numpy.core.fromnumeric import shape
from models import Bucket, BudgetStat

class LP():

     def __init__(self, params: Dict[str, Tuple[float]]):
          np.set_printoptions(formatter={'float': lambda x: "{0:0.2f}".format(x)})
          self.setup(params)

     def setup(self, params: Dict[str, Tuple[float]]):
          self.A = self.create_A_matrix(params)
          self.b = self.create_b_matrix(params).T
          self.c = self.create_c_matrix(params)

     def solve(self):
          """Solves the LP"""

          A = self.A
          b = self.b
          c = self.c

          size = len(c[0])
          x = cp.Variable(shape=(size, 1), name='x')

          prob = cp.Problem(cp.Minimize(c @ x), [A @ x >= b])
          prob.solve()

          self.result = x.value
          return x.value

     def create_A_matrix(self, params: Dict[str, Tuple[float]]):

          # params = params[1:]
          rows = []
          for i in range(1, len(params)):

               lower_constraint = np.zeros(shape=(len(params), 1), dtype=int)
               upper_constraint = np.zeros(shape=(len(params), 1), dtype=int)

               lower_constraint[0] = 1
               lower_constraint[i] = 1
               upper_constraint[0] = 1
               upper_constraint[i] = -1

               rows.append(lower_constraint)
               rows.append(upper_constraint)

          util = -np.ones(shape=(len(params), 1))
          util[0][0] = 0
          rows.append(util)

          # print(np.array(rows).squeeze(axis=2).shape)
          return np.array(rows).squeeze(axis=2)

     def create_b_matrix(self, params: Dict[str, float]):
          rows = []
          row = []
          ranges = list(params.items())
          for i in range(1, len(ranges)):
               row.append(ranges[i][1][0])
               row.append(-ranges[i][1][1])

          income = list(params.items())[0]
          row.append(-income[1][0])
          rows.append(row)

          # print(np.array(rows).shape)
          return np.array(rows)

     def create_c_matrix(self, params: Dict[str, float]):
          constraints = []
          row = np.zeros(shape=(len(params), 1))
          row[0] = 1
          constraints.append(row)

          # print(np.array(constraints).squeeze(axis=2).shape)
          return np.array(constraints).squeeze(axis=2)

     def get_stats(self, params):
          categories: List[Bucket] = []
          items = list(params.items())

          for i in range(1, len(self.result)):
               bucket = self.__get_values(items[i], self.result[i])
               categories.append(bucket)

          # this can be better since we dont know if income is always fist
          # this is an assumption for testing
          income: BudgetStat = BudgetStat(
               name=items[0][0],
               value=round(float(items[0][1][0]), 2),
          )
          extra: BudgetStat = BudgetStat(
               name="extra",
               value=round(items[0][1][0] - sum(self.result)[0], 2)
          )
          total: BudgetStat = BudgetStat(
               name="total",
               value= round(sum(self.result)[0], 2)
          )

          upper_bound = 0
          lower_bound = 0
          for i in range(1, len(items)):
               upper_bound += items[i][1][1]
               lower_bound += items[i][1][0]

          sum_lower_bound: BudgetStat = BudgetStat(name="sum of lower", value=lower_bound)
          sum_upper_bound: BudgetStat = BudgetStat(name="sum of upper", value=upper_bound)

          categories.extend([income, extra, total, sum_lower_bound, sum_upper_bound])

          return categories

     def __get_values(self, item, result):
           bucket: Bucket = Bucket(
                name=item[0],
                result=round(float(result[0]), 2),
                lower=round(float(item[1][0]), 2),
                upper=round(float(item[1][1]), 2)
           )

           return bucket


# TODO: Add bounds to json response
# TODO: Consider another round of optimization for the "extra"


