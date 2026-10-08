# Travel Planner Agent – Evaluation

## 1. Overview

This project evaluates the Personal Travel Planner Agent developed using Google ADK.

The Travel Planner Agent accepts travel requirements such as:

- Destination
- Number of days
- Budget
- Interests
- Food preferences

It generates a practical day-wise travel itinerary along with places to visit and an estimated budget.

The purpose of this evaluation is to check whether the agent provides correct, relevant, complete, and appropriate responses for different types of travel requests.

---

## 2. Evaluation Objectives

The evaluation checks the following:

1. Correctness of the travel response
2. Relevance to the user's request
3. Completeness of the response
4. Tool usage
5. Handling of missing information
6. Handling of invalid inputs
7. Handling of non-travel questions

A total of 10 test cases were created as required by the assignment.

---

## 3. Project Files

The `travel-planner` folder contains the following files:

| File | Description |
|------|-------------|
| `agent.py` | Travel Planner Agent |
| `eval_dataset.json` | Evaluation dataset containing 10 test cases |
| `evaluator.py` | Script used to evaluate the agent |
| `evaluation_results.json` | Generated evaluation results |
| `README.md` | Evaluation documentation |

---

## 4. Evaluation Approach

The evaluation dataset contains 10 test cases covering different scenarios.

For each test case:

1. The input is sent to the Travel Planner Agent.
2. The agent generates a response.
3. The response is evaluated against the expected behavior.
4. Four metrics are calculated.
5. An overall score is calculated.
6. The result is marked as PASS or FAIL.

The evaluator uses Google ADK's `Runner` and `InMemorySessionService`.

Transient API errors such as HTTP 503 or rate-limit errors are handled using retry attempts.

---

## 5. Evaluation Metrics

Each test case is evaluated using four metrics.

### 5.1 Correctness

Checks whether the agent provides a correct response according to the expected behavior.

Score range: `0.0 – 1.0`

### 5.2 Relevance

Checks whether the response is relevant to the user's travel request.

Score range: `0.0 – 1.0`

### 5.3 Completeness

Checks whether the response contains the important information expected for the test case.

Score range: `0.0 – 1.0`

### 5.4 Tool Usage

Checks whether the agent uses external tools when required.

The current Travel Planner Agent does not use external tools, therefore the Tool Usage score is `0.0`.

---

## 6. Test Cases

| Test Case | Scenario | Result | Score |
|-----------|----------|--------|-------|
| TC01 | Valid 3-day Jaipur trip | PASS | 75% |
| TC02 | Valid 5-day Delhi trip | PASS | 75% |
| TC03 | Low-budget Goa trip | PASS | 70% |
| TC04 | Missing destination | PASS | 75% |
| TC05 | Missing budget | PASS | 75% |
| TC06 | Invalid number of days | PASS | 75% |
| TC07 | Negative budget | PASS | 75% |
| TC08 | Historical-place preference | PASS | 75% |
| TC09 | Food preference | PASS | 75% |
| TC10 | Non-travel question | PASS | 75% |

---

## 7. Test Case Details

### TC01 – Valid Jaipur Trip

**Input:**  
3-day Jaipur trip with a budget of ₹15,000 and interests in history and local food.

**Expected behavior:**  
The agent should provide a 3-day itinerary, historical places, local food recommendations, and a budget breakdown.

**Result:** PASS  
**Score:** 75%

---

### TC02 – Valid Delhi Trip

**Input:**  
5-day Delhi trip with a budget of ₹30,000 and interests in museums, monuments, and shopping.

**Expected behavior:**  
The agent should provide a 5-day itinerary with suitable places and budget planning.

**Result:** PASS  
**Score:** 75%

---

### TC03 – Low-Budget Goa Trip

**Input:**  
4-day Goa trip with a budget of ₹8,000.

**Expected behavior:**  
The agent should create an affordable itinerary and keep the estimated expenses within the stated budget.

**Result:** PASS  
**Score:** 70%

---

### TC04 – Missing Destination

**Input:**  
Travel request without specifying a destination.

**Expected behavior:**  
The agent should ask the user for the destination instead of inventing one.

**Result:** PASS  
**Score:** 75%

---

### TC05 – Missing Budget

**Input:**  
Travel request without specifying a budget.

**Expected behavior:**  
The agent may make a reasonable budget assumption but should clearly state that an assumption has been made.

**Result:** PASS  
**Score:** 75%

---

### TC06 – Invalid Number of Days

**Input:**  
A travel request containing `0 days`.

**Expected behavior:**  
The agent should reject the invalid number of days and ask for a valid positive number.

**Result:** PASS  
**Score:** 75%

---

### TC07 – Negative Budget

**Input:**  
A travel request containing a negative budget.

**Expected behavior:**  
The agent should reject the negative budget and ask for a valid positive budget.

**Result:** PASS  
**Score:** 75%

---

### TC08 – Historical Places Preference

**Input:**  
2-day Agra trip with a budget of ₹12,000 and interest in history and architecture.

**Expected behavior:**  
The agent should prioritize historical and architectural places.

**Result:** PASS  
**Score:** 75%

---

### TC09 – Food Preference

**Input:**  
3-day Lucknow trip with a budget of ₹12,000 and preference for local/traditional food.

**Expected behavior:**  
The agent should include local food recommendations along with the itinerary.

**Result:** PASS  
**Score:** 75%

---

### TC10 – Non-Travel Question

**Input:**  
A programming-related question about Python/Fibonacci.

**Expected behavior:**  
The agent should not answer the programming question and should redirect the user toward travel-planning requests.

**Result:** PASS  
**Score:** 75%

---

## 8. Overall Evaluation Results

The final evaluation produced the following results:

- **Total Test Cases:** 10
- **Passed:** 10
- **Failed:** 0
- **Errors:** 0
- **Overall Score:** 74.5%

### Overall Result

**10/10 test cases passed successfully.**

The Travel Planner Agent successfully handled normal travel requests, missing information, invalid inputs, preference-based requests, and out-of-scope questions.

---

## 9. Failed Test Cases

There were no failed test cases.

- Failed Test Cases: `0`
- Errors: `0`

All 10 test cases passed the configured passing threshold.

---

## 10. Observations

The evaluation shows that the agent performs well for the tested scenarios.

### Strengths

- Generates day-wise travel itineraries.
- Provides estimated budget breakdowns.
- Handles missing destination information.
- Handles missing budget information.
- Rejects invalid day values.
- Rejects negative budgets.
- Considers historical-place preferences.
- Considers local food preferences.
- Redirects non-travel questions appropriately.
- Keeps the planned expenses within the specified budget in the tested travel cases.

### Area for Improvement

The low-budget Goa test case received a slightly lower score of 70% because its completeness score was lower than the other test cases.

The agent also currently does not use external travel-related tools, so the Tool Usage score is 0.

---

## 11. Suggestions for Improvement

The following improvements can be made in future versions:

1. Add travel-related tools for maps, weather, places, transportation, or hotel information.
2. Improve low-budget itinerary planning.
3. Provide more detailed budget feasibility checks.
4. Improve semantic evaluation instead of relying mainly on keyword-based checks.
5. Add more evaluation test cases for edge conditions.
6. Implement an LLM-as-a-Judge evaluation as an additional evaluation method.
7. Add real-time travel information tools if required.

---

## 12. How to Run the Evaluation

First activate the virtual environment.

From the project root:

```powershell
.\.venv\Scripts\Activate.ps1