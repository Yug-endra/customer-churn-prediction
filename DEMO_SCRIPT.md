# Demo Script - one page

Keep this open on your phone or a second screen during the review.

---

## Before you start

```powershell
cd D:\Internship
streamlit run app.py
```

If the port is busy: `streamlit run app.py --server.port 8502`

Open <http://localhost:8501>. Use a **fresh browser tab** so the inputs are at their
defaults. If the numbers below do not match, refresh the page once.

---

## The 90-second demo

### Step 1 - Open on "Risk assessment" (10 seconds)

**Say:** "This is the live app. It loads the same saved model from the report."

Confirm the default profile shows:

- **71.3% - High risk**
- Contract: Month-to-month
- Internet: Fiber optic
- Tenure: 12 months
- Payment: Electronic check
- No tech support, no online security

### Step 2 - Point at the factor chips (15 seconds)

**Say:** "The score is not a black box. These chips show the risk patterns behind it:
month-to-month contract, new customer, fiber optic, electronic check, no support and no
security. The green chip shows a protective factor: the customer has dependents."

### Step 3 - Scroll to "What if we intervened?" (25 seconds)

Point to each card in order:

| Change | New risk | Change |
|---|---:|---:|
| One-year contract | **54.6%** | -16.7 points |
| Two-year contract | **34.2%** | -37.1 points |
| Automatic credit-card payment | **63.0%** | -8.3 points |

**Say:** "This is the part a business user can act on. Moving this customer to a two-year
contract is associated with a drop from 71.3% to 34.2%. These are model-based associations,
not proven causes, so the next step would be an A/B test."

Do **not** change the sliders unless you want to. The numbers above depend on the defaults.

### Step 4 - Click "Model performance" (20 seconds)

Point to:

- **ROC-AUC 0.846**
- **Recall 79.4%**
- Confusion matrix: **297 of 374 churners caught**, 77 missed, 290 false alarms.

**Say:** "On 1,409 customers the model never saw, it caught about four out of five churners.
The false alarms are the tradeoff we accepted because a missed churner is expensive."

### Step 5 - Click "Data insights" (15 seconds)

Point to the contract chart.

**Say:** "This is the insight that drives the recommendation: 42.7% churn on month-to-month,
versus 2.8% on two-year contracts."

### Step 6 - Close (5 seconds)

**Say:** "The model is a decision aid, not a replacement for the retention team."

---

## If something goes wrong

| Problem | Fix |
|---|---|
| Page is blank or stale | Refresh once |
| "Connection error" | The server stopped; run `streamlit run app.py` again |
| Port already in use | `streamlit run app.py --server.port 8502` |
| Numbers look different | Refresh the page to reset the widgets |
| App will not start at all | Use slide 13 and say the code is in the repository |

Never debug in front of the reviewer. Switch to the slide screenshot and keep talking.

---

## Exact default profile (for reference)

| Field | Default |
|---|---|
| Gender | Female |
| Senior citizen | No |
| Partner | Yes |
| Dependents | Yes |
| Phone service | Yes |
| Multiple lines | No |
| Internet service | Fiber optic |
| Online security / backup / protection | No |
| Tech support | No |
| Streaming TV / movies | No |
| Contract | Month-to-month |
| Paperless billing | Yes |
| Payment method | Electronic check |
| Tenure | 12 months |
| Monthly charges | $70.00 |
| Predicted risk | **71.3%** |
