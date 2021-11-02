

# income = 2367.72 * 2
# constraints = [
#     [600, 600.01],  # rent
#     [150, 150.01],  # util
#     [112, 400],     # WPI loan
#     [300, 500],     # fed loan
#     [300, 1000],    # savings
#     [300, 1000],    # invest
#     [200, 500],     # Emergency
#     [80, 80.01],    # gym
#     [200, 300],     # groceries
# ]


# Z = []
# for i in range(len(constraints)):
#     Z.append(((vals[i] - constraints[i][0]) / (constraints[i][1] - constraints[i][0])) / len(constraints))

# print(Z)
# print(sum(Z))
# print("ratio: " + str(ratio))


### =======================================================

### IDEA


class Budget():

    def __init__(self, cash, score, X):
        self.cash = cash
        self.score = score
        self.X = X
        # self.W = W

    def adjust_params(self, differences):
        # adjust cash
        score = []
        for i in range(len(differences)):
            if differences[i] > 1:
                score.append(self.score[i])
            else:
                self.cash -= self.X[i][0]
        self.W = [(score[i] / sum(score)) for i in range(len(score))]

    def error(self, values):
        result = 0
        for i in range(len(values)):
            h = (self.cash*self.W[i] - values[i])**2
            result += h
        return result / (2 * len(values))

    def twiddle(self):
        estimates = self.X
        diff = [estimates[i][1] - estimates[i][0] for i in range(len(estimates))]
        self.adjust_params(diff)
        vals = [estimates[i][0] for i in range(len(estimates)) if diff[i] > 0]
        dp = [1 for i in range(len(vals))]
        best_error = self.error(vals)
        threshhold = 0.001

        while sum(dp) > threshhold:
            for i in range(len(vals)):
                vals[i] += dp[i]
                err = self.error(vals)

                if err < best_error:
                    best_error = err
                    dp[i] *= 1.1
                else:
                    vals[i] -= 2 * dp[i]
                    err = self.error(vals)

                    if err < best_error:
                        best_error = err
                        dp[i] *= 1.05
                    else:
                        vals[i] += dp[i]
                        dp[i] *= 0.95
        return vals, best_error


CASH = 1000
X = [[400, 400],
     [200, 500],
     [200, 500],
     [200, 400]]
SCORE = [5, 4, 4, 2]

# ideal score here is 400, 200, 200, 200 if we want to base off of score
# That, or if we cant meet the constraint, suggest we drop the min to something better or rework how score affects twiddle

# score may look like the probability distribution of the rows. it IS if we can meet the quota given enough cash. If not, it needs to be a WEIGHTING to distribute money into each row
# For example, looking at the last three rows since the first is a fixed payment:
    # We have 600 to spread out, with minimums being 200 for the last three rows. Since the scores here are 4, 4, 3, we would like to have more weighton rows 2 and 3 since they are score 4. But since we only have 600 left, and the total of the minimums constraint are also 600, we are better off spreading the money evenly across all three. This satisfies the constraint over the scoring.
    # Now, we could go back and forth over to choose contraint or score. given an example like above, what probably is BEST is to give the current prices, and a suggestion to either lower the constraint for row 4 (if we want to meet the score requirements) or give it a higher score (if we want to meet the constraint requirements)

#  At the end of the day, this works pretty nicely! Simple to do, and the only decisions to make are coming up with minimum contraints for budget items and a score (1 : low priority -- 5 : highest priority). The rest does the work (for now, loans would be REALLY nice to come up with a better error)

# Now try increasing the income and let it use up all the money! Does it go past the max constraints? 
W = [(SCORE[i] / sum(SCORE)) for i in range(len(SCORE))]


test = Budget(CASH, SCORE, X)

income = 2367.72 * 2
conts = [[600, 600],
         [150, 150],
         [120, 120],
         [475, 475],
         [500, 1000],
         [500, 1000],
         [400, 800],
         [200, 500],
         [200, 300],
         [200, 400]]
    
weights = [5, 5, 5, 5, 4, 4, 4, 2, 3, 2]
test2 = Budget(income, weights, conts)

estimates, error = test2.twiddle()
print(f"Estimated prices: ")
print(estimates)
print("Sum of prices: " + str(sum(estimates)))
