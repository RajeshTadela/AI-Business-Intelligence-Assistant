import pandas as pd
from ai.insight_generator import generate_insights

df = pd.DataFrame({
    "Product": ["P11", "P04"],
    "Revenue": [2112502, 2090242]
})

result = generate_insights(
    "Show top 2 products by revenue",
    df
)

print(result)