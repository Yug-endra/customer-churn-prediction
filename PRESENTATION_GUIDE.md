# Presentation Guide

Everything you need to present the project confidently, even if the modeling details are
new to you. Read this once end to end, then practise the 10-minute run-of-show twice.

---

## 0. If you only have three hours

Do this in order. Do not try to learn everything.

| Time | What to do |
|---|---|
| 0:00-0:20 | Run the app. Click every tab. Read `DEMO_SCRIPT.md`. |
| 0:20-0:45 | Read the 60-second version and memorise the nine numbers below. |
| 0:45-1:30 | Open the slide deck and read the slide-by-slide script out loud. |
| 1:30-2:00 | Read the plain-English concepts section. |
| 2:00-2:30 | Read the likely Q&A. Say each answer out loud once. |
| 2:30-2:50 | Practise the full 10-minute run-of-show twice. |
| 2:50-3:00 | Rehearse the demo clicks once, then stop. |

If you blank during the presentation, fall back to these five facts:

1. "One in four customers churn - 26.5%."
2. "The model has a ROC-AUC of 0.846 on customers it never saw."
3. "It catches about 79% of customers who actually leave."
4. "Month-to-month customers churn at 42.7%, versus 2.8% on two-year contracts."
5. "The app turns the score into a what-if tool for retention actions."

---

## 1. The 60-second version

> "I built a customer churn prediction system for a telecom company. The dataset has 7,043
> customers, and about one in four churned. I cleaned the data, explored what separates
> churners from loyal customers, and compared three machine learning models. Logistic
> Regression won with a ROC-AUC of 0.846, and it catches about 79% of customers who
> actually leave. I then turned the model into a live app that shows a customer's risk,
> explains the factors behind it, and simulates how contract or support changes would
> reduce that risk. The main insight is that commitment and support matter more than
> feature count: month-to-month customers churn at 42.7%, versus 2.8% on two-year
> contracts."

That is the whole project in one breath. Everything else is detail.

---

## 2. Numbers to memorize

You do not need to memorize every number. Learn these nine:

| Number | Meaning |
|---|---|
| **7,043** | Customers in the dataset |
| **26.5%** | Overall churn rate |
| **80/20** | Train/test split (5,634 / 1,409) |
| **0.846** | ROC-AUC on unseen test data |
| **79.4%** | Recall - share of real churners caught |
| **50.6%** | Precision - share of flags that were real churners |
| **42.7% vs 2.8%** | Churn on month-to-month vs two-year contracts |
| **297 of 374** | Churners caught in the test set |
| **71.3% -> 34.2%** | Demo risk before/after a two-year contract |

If you remember only three: **26.5% churn**, **0.846 ROC-AUC**, **79.4% recall**.

---

## 3. Ten-minute run of show

| Time | Slide | What to do |
|---|---|---|
| 0:00-0:45 | 1 | Introduce yourself and the one-sentence goal |
| 0:45-1:30 | 3 | Explain why churn matters and the business question |
| 1:30-2:15 | 4 | Describe the dataset and the 26.5% imbalance |
| 2:15-3:15 | 5 | Walk the seven-step pipeline quickly |
| 3:15-4:45 | 6-7 | Two key insights: contract/tenure, then services/billing |
| 4:45-5:30 | 8 | Explain the three engineered features and clean validation |
| 5:30-6:45 | 9-10 | Model comparison, results and confusion matrix |
| 6:45-7:30 | 11 | The accuracy trap - this is the strongest slide |
| 7:30-8:15 | 12 | What drives the model |
| 8:15-9:15 | 13 | Live demo (or screenshots if the demo fails) |
| 9:15-10:00 | 14-16 | Recommendations, limitations, thank you |

If you are cut to **five minutes**: title, problem, one insight (contract/tenure), results,
demo, one recommendation. Skip slides 5, 8 and 12.

Do not read the slides. The slides are there to support you. Each slide has one sentence
you should land clearly.

---

## 4. Slide-by-slide speaking script

### Slide 1 - Title
**Say:** "Good morning. My project is customer churn prediction. The goal was to identify
customers who are likely to leave before they actually do, and to explain what the business
can do about it. The headline result is a ROC-AUC of 0.846, and the model catches about 79%
of customers who churn."

### Slide 2 - Agenda
**Say:** "I'll cover the business problem, the data, the methodology, the key insights, the
model results, and then a live demo and recommendations."

Keep this under 15 seconds.

### Slide 3 - The business problem
**Say:** "Acquiring a customer is usually more expensive than keeping one, and in this
dataset about one in four customers left. A retention team cannot call all 7,000 customers,
so they need a ranked list: who is most at risk, why, and what might help. That is the
question this project answers."

Point to the three stats: 26.5%, 7,043, 1,409.

### Slide 4 - The data
**Say:** "The data is the public IBM Telco Customer Churn dataset: 7,043 customers and 21
columns covering demographics, services, account details and billing. The target is whether
the customer churned. The main challenge is imbalance: 73.5% stayed and 26.5% left. I also
fixed 11 blank TotalCharges values, all for brand-new customers, and dropped the customer ID
because it is just a random identifier."

### Slide 5 - Methodology
**Say:** "The pipeline has seven steps: clean, explore, engineer features, split, train,
evaluate, and deploy. Two design choices matter. First, all preprocessing is inside the
model pipeline, so it is fitted only on training data - no leakage. Second, the test set is
touched once, at the very end, so the reported numbers are honest."

Do not explain every step. Move quickly.

### Slide 6 - Key insight 1
**Say:** "The strongest signal is contract and tenure. Month-to-month customers churn at
42.7%, versus 2.8% on two-year contracts - a fifteen-fold difference. Churn is also
concentrated in the first year. The average churner has 18 months of tenure; the average
customer who stays has 37.6. This tells us the onboarding window is where retention effort
should go."

### Slide 7 - Key insight 2
**Say:** "Services and billing tell the same story. Fiber optic customers churn at 41.9%,
versus 7.4% with no internet. Electronic-check payers churn at 45.3%, versus about 15% on
automatic payments. Customers without tech support or online security churn at around 42%,
versus about 15% with them. The pattern is commitment and perceived support, not just
feature count."

### Slide 8 - Feature engineering
**Say:** "I added three features a business audience can understand: how many services a
customer has, their average monthly spend, and whether they are in their first six months.
The preprocessing - median imputation, scaling and one-hot encoding - is inside the
pipeline, so the app applies exactly the same steps as training. That is how I avoided a
very common production bug."

### Slide 9 - Model comparison
**Say:** "I compared three models with five-fold cross-validation. Logistic Regression and
Random Forest were essentially tied on ROC-AUC, 0.847 versus 0.846. Gradient Boosting was
lower at 0.827. I chose Logistic Regression because it had the highest cross-validated
ROC-AUC, the highest recall - 79% versus 74% - and it is much easier to explain. On a
dataset of this size, the more complex models did not buy us anything."

If asked why Random Forest has a higher F1: "It does, 0.629 versus 0.618. But it catches five
percentage points fewer churners. For retention, recall matters more, and the selection
metric was cross-validated ROC-AUC."

### Slide 10 - Results
**Say:** "On the 1,409 customers the model never saw, it achieved a ROC-AUC of 0.846 and a
recall of 79.4%. Out of 374 actual churners, it caught 297 and missed 77. It also raised 290
false alarms. That tradeoff is deliberate: missing a churner usually costs more than
offering a retention discount to someone who would have stayed."

### Slide 11 - The accuracy trap
**Say:** "This is the question people often ask: why is accuracy only 74%? If I predicted
that everyone stays, I would be 73.5% accurate while catching zero churners. Our model has
almost the same accuracy but catches 79% of churners. That is the difference between a
useless model and a useful one. This is why I optimize ROC-AUC and recall, not accuracy."

Pause here. This slide usually earns nods.

### Slide 12 - Drivers
**Say:** "To explain the model, I used permutation importance: shuffle one feature and see
how much ROC-AUC drops. The top drivers are tenure, contract, internet service, monthly
charges and the new-customer flag. That matches the exploratory analysis, which gives us
confidence the model learned real behavior rather than noise."

### Slide 13 - Live demo
**Say:** "The app loads the same saved pipeline - there is no separate logic in the demo.
I'll show three things: set a customer profile, read the risk score and the factors behind
it, and use the what-if panel to see how contract or support changes reduce the risk."

Then follow the click-by-click steps in `DEMO_SCRIPT.md`. Keep the demo under 90 seconds.

### Slide 14 - Recommendations
**Say:** "The model suggests four practical plays: focus on the first six months, convert
month-to-month customers to annual contracts, bundle tech support and online security, and
move customers to automatic payments. These are associations, not proven causes, so the
next step is to test them with an A/B test before scaling."

### Slide 15 - Limitations and next steps
**Say:** "I want to be honest about the limits. This is one company and one period, so
results may not transfer. The data is observational, so the what-if results are
associations, not causes. The 0.50 threshold is a starting point, not an optimized business
decision. Next steps are SHAP explanations, monitoring and retraining, A/B tests, and adding
customer lifetime value."

### Slide 16 - Thank you
**Say:** "To summarize: one in four customers churn, the behavior is predictable, and the
model catches about 79% of churners with a ROC-AUC of 0.846. The app turns that into a
practical what-if tool. I'm happy to take questions."

---

## 5. Plain-English concepts

### First, the 22 inputs the model actually sees

**Numeric (7)**

- `SeniorCitizen` (0/1)
- `tenure` (months)
- `MonthlyCharges`
- `TotalCharges`
- `NumServices` - engineered: count of active services
- `AvgMonthlySpend` - engineered: total charges / tenure
- `IsNewCustomer` - engineered: tenure of 6 months or less

**Categorical (15)**

- Customer: `gender`, `Partner`, `Dependents`
- Services: `PhoneService`, `MultipleLines`, `InternetService`, `OnlineSecurity`,
  `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`, `StreamingMovies`
- Account: `Contract`, `PaperlessBilling`, `PaymentMethod`

**Dropped:** `customerID` (random identifier). **Target:** `Churn` (1 = left, 0 = stayed).

The categorical fields are one-hot encoded, so the model actually sees more than 22
columns after preprocessing. The 22 above are the business inputs.

**A note on DeviceProtection.** In the raw data, customers with device protection churn at
22.5%, versus 39.1% without it - it looks protective. In the model, its own coefficient is
also slightly protective (odds ratio about 0.95). But the app derives `NumServices` from the
service toggles, so switching DeviceProtection to Yes also adds one to `NumServices`.
`NumServices` has a positive coefficient, which can offset the protective effect. That is why
the risk can creep up by a point or so. It is a feature-interaction artifact, not evidence
that device protection causes churn.

Read the concepts below once so the vocabulary feels natural.

**Churn.** A customer leaving or cancelling. Here it is a yes/no label: 1 = churned,
0 = stayed.

**Feature.** An input variable used to predict. Tenure, contract type and monthly charges
are features.

**Target.** The thing being predicted. Here it is `Churn`.

**Train/test split.** The model learns on the training rows and is tested on rows it has
never seen. This is how we estimate how it will perform on new customers. We used 80%
training and 20% testing.

**Stratified split.** A split that keeps the same churn rate in both parts. Without it, a
random split could put too many churners in one side and distort the results.

**Cross-validation.** Split the training data into five parts; train on four and validate
on the fifth, five times. Average the scores. It gives a more stable estimate than a single
split and is used for model selection. The test set stays untouched.

**Data leakage.** When information from the test set or the target sneaks into training.
It makes results look better than they really are. Keeping preprocessing inside the pipeline
and touching the test set once prevents it.

**Class imbalance.** One class is much more common. Here 73.5% stayed and 26.5% churned,
so accuracy alone is misleading.

**Logistic Regression.** A simple model that estimates the probability of a yes/no outcome
by combining the features with learned weights. It is popular because it is fast, stable
and interpretable.

**Random Forest.** Many decision trees trained on random subsets of the data, then averaged.
It captures nonlinear patterns but is harder to explain.

**Gradient Boosting.** Trees built one after another, each correcting the previous one's
mistakes. Powerful on large datasets, but it can underperform on smaller ones like this.

**ROC curve.** A plot of true positive rate versus false positive rate at every possible
threshold. The closer the curve is to the top-left corner, the better.

**ROC-AUC.** The area under the ROC curve. 0.5 is random guessing, 1.0 is perfect. It
measures how well the model ranks at-risk customers above safe ones, independent of a
specific threshold. Ours is 0.846.

**Precision.** Of the customers we flagged as churners, what share actually churned? Ours is
50.6%. Low precision means false alarms.

**Recall.** Of the customers who actually churned, what share did we catch? Ours is 79.4%.
Low recall means missed churners.

**F1 score.** The harmonic mean of precision and recall. A single balanced score, useful when
both types of error matter.

**Confusion matrix.** A 2x2 table of actual versus predicted outcomes: true positives, true
negatives, false positives and false negatives.

**Threshold.** The probability cutoff for flagging someone. At 0.50, a customer with a 50%+
predicted risk is flagged. Lowering it catches more churners but raises more false alarms.

**Permutation importance.** Shuffle one feature, see how much the score drops. A big drop
means the model relies on that feature.

**Pipeline.** A single object that applies preprocessing and then the model. It guarantees
training and production use the same steps.

**Overfitting.** When a model memorizes the training data and fails on new data. We guard
against it with a hold-out test set, cross-validation and a relatively simple model.

---

## 6. Likely questions and strong answers

**Q1. Why did you choose this project?**
A: "Churn is a clean, measurable business problem with a clear payoff. It also lets me show
the full data science workflow - cleaning, exploration, modeling, evaluation and deployment -
rather than just a model in a notebook."

**Q2. Why Logistic Regression instead of a more advanced model?**
A: "It had the best cross-validated ROC-AUC, the best recall, and it is the easiest to
explain. Random Forest was statistically tied on ROC-AUC but caught five percentage points
fewer churners. On 7,000 rows, extra complexity did not help."

**Q3. What is ROC-AUC, in one sentence?**
A: "It measures how well the model ranks at-risk customers above safe ones across all
thresholds. 0.5 is random, 1.0 is perfect, and we got 0.846."

**Q4. Why is your accuracy only 74%?**
A: "Because 73.5% of customers stay, accuracy is dominated by the majority class. A model
that predicts 'everyone stays' is 73.5% accurate and catches zero churners. Our model has
similar accuracy but catches 79% of churners, which is the useful outcome."

**Q5. What is the difference between precision and recall?**
A: "Precision asks: of the customers we flagged, how many really churned? Recall asks: of
all the customers who churned, how many did we catch? We prioritized recall because missing
a churner is usually more expensive than a false alarm."

**Q6. Why is recall more important than precision here?**
A: "A missed churner is lost revenue. A false alarm costs a retention call or a small
discount. If retention actions are cheap relative to customer value, it is better to flag
more people. The business can adjust the threshold to match its cost structure."

**Q7. How did you handle missing data?**
A: "Only TotalCharges had missing values: 11 blanks, all for customers with zero tenure.
I converted the column to numeric and filled those with the monthly charge. Numeric gaps in
general are handled by median imputation inside the pipeline."

**Q8. How did you avoid overfitting?**
A: "Three ways: a hold-out test set that was touched only once, five-fold cross-validation
for model selection, and a relatively simple model. I also kept preprocessing inside the
pipeline to avoid leakage."

**Q9. What is cross-validation and why five folds?**
A: "The training data is split into five parts. The model trains on four and validates on
the fifth, five times, and the scores are averaged. Five folds are a common balance between
stability and compute cost."

**Q10. Why an 80/20 split?**
A: "It gives enough data to train - 5,634 rows - while keeping a test set of 1,409 rows,
which is large enough to estimate performance reliably. The split is stratified to preserve
the churn rate."

**Q11. Which features mattered most?**
A: "Tenure, contract type, internet service, monthly charges and the new-customer flag.
Contract and tenure are also the most actionable: they point to onboarding and annual
contracts."

**Q12. Did you do feature selection?**
A: "I did not run an automated feature-selection step. I used domain reasoning to keep the
raw features plus three engineered ones, and I checked permutation importance afterward. The
top features are coherent and match the EDA, so there was no strong reason to prune further."

**Q13. How would this work in production?**
A: "The saved pipeline takes raw customer fields and returns a probability. It could run
nightly, write scores to the CRM, and surface a ranked list to the retention team. You would
also need monitoring for drift, a retraining schedule, and a feedback loop on which offers
worked."

**Q14. What are the limitations?**
A: "One company and one period, so transfer is uncertain. Observational data, so associations
are not causal. A fixed 0.50 threshold that is not cost-optimized. No lifetime value,
competitor or market data. And the dataset is not recent."

**Q15. What would you do with more time?**
A: "Add SHAP for per-customer explanations, test the retention offers with A/B tests, add
customer lifetime value to prioritize by profit, and set up monitoring and retraining."

**Q16. Why not use a neural network?**
A: "With 7,000 rows and mostly tabular, low-dimensional data, a neural network is unlikely to
beat a well-tuned linear model or a forest. It would also be harder to explain. The simpler
model already reaches 0.846 ROC-AUC."

**Q17. What does the what-if panel actually prove?**
A: "It shows how the model's score changes when one input changes, holding everything else
constant. That is an association, not proof of causation. To claim causation, we would need
an experiment or a causal design."

**Q18. How do you know the model is not just memorizing?**
A: "The reported numbers come from 1,409 customers the model never saw. Cross-validation on
the training set gave a similar ROC-AUC, 0.847, which is consistent with the test result of
0.846. That consistency is evidence against memorization."

**Q19. Why did you drop customerID?**
A: "It is a random identifier. It has no business meaning and could let the model memorize
individual customers instead of learning behavior."

**Q20. What if the reviewer asks to see the code?**
A: "Open `src/train.py`. It is organized in the same order as the presentation: load and
clean, EDA, feature engineering, preprocessing, models, evaluation and saving. The app is in
`app.py` and loads the saved pipeline."

**Q21. Why does adding device protection sometimes increase the predicted risk?**
A: "Good catch. In the raw data, device protection is associated with lower churn - 22.5%
versus 39.1% without it. The model's own coefficient for it is also slightly protective, with
an odds ratio of about 0.95. The reason the app can show a small increase is that adding a
service also raises the derived `NumServices` feature, which has a positive coefficient. So
two inputs change at once. It is a feature-interaction artifact, not evidence that device
protection causes churn. In a production what-if tool I would hold the derived feature fixed
or show the two effects separately."

**Q22. What features does the model use?**
A: "Seven numeric inputs - senior citizen, tenure, monthly charges, total charges, number of
services, average monthly spend, and a new-customer flag. Fifteen categorical inputs covering
demographics, services, contract and billing. The customer ID is dropped. That is 22 business
inputs, which become more columns after one-hot encoding."

### If you do not know an answer

Do not improvise. Say:

> "That is a good question. I did not test that specifically, but based on what I did, my
> expectation would be ___. I would want to check it before making a claim."

Then move on. Reviewers respect honest boundaries far more than confident nonsense.

---

## 7. Demo instructions

Full click-by-click steps are in `DEMO_SCRIPT.md`. The short version:

1. Open <http://localhost:8501>.
2. Leave the default profile: month-to-month, fiber optic, 12 months, electronic check,
   no support, no security. It should show **71.3% high risk**.
3. Point at the factor chips: month-to-month contract, new customer, fiber optic,
   electronic check, no support, no security.
4. Scroll to "What if we intervened?" and read the three cards:
   one-year contract **54.6%**, two-year contract **34.2%**, automatic card payment **63.0%**.
5. Click **Model performance** and point to ROC-AUC **0.846**, recall **79.4%**, and the
   confusion matrix: **297 of 374 churners caught**.
6. Click **Data insights** and show the contract chart: **42.7% vs 2.8%**.
7. Close with: "These are model-based associations; the next step is an A/B test."

### If the demo breaks

- Refresh the page once.
- If the server is down, run `streamlit run app.py` in the project folder.
- If the port is busy, add `--server.port 8502`.
- If it still fails, go to slide 13 (the screenshot) and say: "I have the app and full code
  in the repository; let me walk you through the same flow on the screenshot." Do not debug
  in front of the reviewer.

---

## 8. Final checklist

**The day before**
- [ ] Confirm the slide identity is correct (Yugendra Pujari, Avishkarana Andhra Summer Internship, Bharat Care Life Line Foundation).
- [ ] Run `python src/train.py` once to confirm it still works.
- [ ] Run `streamlit run app.py` and test the default profile.
- [ ] Practise the 10-minute run-of-show twice, out loud.
- [ ] Read the Q&A section once.

**Fifteen minutes before**
- [ ] Start the app and leave it open.
- [ ] Open the PPTX in presenter mode.
- [ ] Close unrelated tabs and notifications.
- [ ] Have `DEMO_SCRIPT.md` open on your phone or a second screen.
- [ ] Water nearby.

**During the presentation**
- [ ] Speak slower than you think you need to.
- [ ] Pause after the accuracy-trap slide.
- [ ] Keep the demo under 90 seconds.
- [ ] It is fine to say "I don't know" and explain how you would find out.

You built a complete project with real data, a validated model, a working app and a clear
business story. That is more than enough to present well.
