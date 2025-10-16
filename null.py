import statsmodels.api as sm
from statsmodels.genmod.generalized_linear_model import GLM
from statsmodels.genmod import families
import pandas as pd

csv = "seance_autizzy_test_results_cleaned_w_negation.csv"
df = pd.read_csv(csv)
file_name = "autizzy_glm_gaussian_null_positive_and_negative.txt"

subdirectory = "gaussian_plots_grouped"

# Assuming you have your data (X, y)
# Define your full GLM
full_model = GLM(y, X, family=families.Gaussian()) # Example with Poisson family
full_results = full_model.fit()

# Define the null model (intercept only)
null_model = GLM(y, sm.add_constant(X[:, 0]*0), family=families.Gaussian()) # X[:,0]*0 creates a column of zeros for the intercept
null_results = null_model.fit()

# Perform the Likelihood Ratio Test
lrt_pvalue = full_results.compare_lr_test(null_results)[1]

print(f"Likelihood Ratio Test p-value: {lrt_pvalue}")