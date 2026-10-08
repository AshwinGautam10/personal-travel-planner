import asyncio
import json
import os

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


# =========================================================
# PATH CONFIGURATION
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

DATASET_FILE = os.path.join(
    BASE_DIR,
    "eval_dataset.json"
)

RESULTS_FILE = os.path.join(
    BASE_DIR,
    "evaluation_results.json"
)

ENV_FILE = os.path.join(
    PROJECT_DIR,
    ".env"
)


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv(ENV_FILE)


# =========================================================
# IMPORT TRAVEL PLANNER AGENT
# =========================================================

from agent import root_agent


# =========================================================
# LOAD EVALUATION DATASET
# =========================================================

with open(
    DATASET_FILE,
    "r",
    encoding="utf-8"
) as file:
    test_cases = json.load(file)


# =========================================================
# BASIC HELPER FUNCTIONS
# =========================================================

def contains_any(text, keywords):
    """
    Return True if at least one keyword appears in text.
    """

    text = text.lower()

    return any(
        keyword.lower() in text
        for keyword in keywords
    )


# =========================================================
# RESPONSE EVALUATION
# =========================================================

def evaluate_response(test_case, response):
    """
    Evaluate the agent response using four metrics:

    1. Correctness
    2. Relevance
    3. Completeness
    4. Tool Usage

    Each metric is scored from 0.0 to 1.0.
    """

    test_id = test_case["test_case_id"]

    expected = test_case["expected_behavior"]

    response_lower = response.lower()

    correctness = 0.0
    relevance = 0.0
    completeness = 0.0

    # Current agent has no external tools.
    tool_usage = 0.0


    # =====================================================
    # TC10 - OUTSIDE AGENT SCOPE
    # =====================================================

    if test_id == "TC10":

        travel_redirect = contains_any(
            response_lower,
            [
                "travel",
                "travel planner",
                "travel-related",
                "travel related",
                "itinerary",
                "trip",
                "destination",
            ]
        )

        programming_content = contains_any(
            response_lower,
            [
                "fibonacci",
                "python code",
                "def fib",
                "program",
                "programming",
                "code",
            ]
        )

        if travel_redirect:
            correctness = 1.0
            relevance = 1.0
        else:
            correctness = 0.0
            relevance = 0.0

        if not programming_content:
            completeness = 1.0
        else:
            completeness = 0.0


    # =====================================================
    # TC04 - MISSING DESTINATION
    # =====================================================

    elif test_id == "TC04":

        destination_missing = contains_any(
            response_lower,
            [
                "destination",
                "where would",
                "which destination",
                "where do you",
                "which city",
                "where are you",
                "destination?",
            ]
        )

        if destination_missing:
            correctness = 1.0
            relevance = 1.0
            completeness = 1.0
        else:
            correctness = 0.0
            relevance = 1.0
            completeness = 0.0


    # =====================================================
    # TC06 - INVALID NUMBER OF DAYS
    # =====================================================

    elif test_id == "TC06":

        invalid_days_detected = contains_any(
            response_lower,
            [
                "0 days",
                "invalid",
                "positive number",
                "valid number of days",
                "number of days must",
                "at least 1 day",
                "days must be",
            ]
        )

        if invalid_days_detected:
            correctness = 1.0
            relevance = 1.0
            completeness = 1.0
        else:
            correctness = 0.0
            relevance = 1.0
            completeness = 0.0


    # =====================================================
    # TC07 - NEGATIVE BUDGET
    # =====================================================

    elif test_id == "TC07":

        negative_budget_detected = contains_any(
            response_lower,
            [
                "negative",
                "invalid budget",
                "valid budget",
                "positive budget",
                "budget cannot",
                "budget must",
                "negative budget",
            ]
        )

        if negative_budget_detected:
            correctness = 1.0
            relevance = 1.0
            completeness = 1.0
        else:
            correctness = 0.0
            relevance = 1.0
            completeness = 0.0


    # =====================================================
    # NORMAL TRAVEL REQUESTS
    # =====================================================

    else:

        # -------------------------------------------------
        # Itinerary
        # -------------------------------------------------

        itinerary_present = contains_any(
            response_lower,
            [
                "day 1",
                "day 2",
                "day-wise",
                "itinerary",
                "morning",
                "afternoon",
                "evening",
            ]
        )


        # -------------------------------------------------
        # Budget
        # -------------------------------------------------

        budget_present = contains_any(
            response_lower,
            [
                "budget",
                "estimated total",
                "accommodation",
                "food",
                "local transport",
                "transportation",
                "entry tickets",
                "miscellaneous",
            ]
        )


        # -------------------------------------------------
        # Places
        # -------------------------------------------------

        places_present = contains_any(
            response_lower,
            [
                "recommended places",
                "places to visit",
                "fort",
                "museum",
                "food",
                "market",
                "palace",
                "monument",
                "bazaar",
                "temple",
                "beach",
            ]
        )


        # -------------------------------------------------
        # Correctness
        # -------------------------------------------------

        correctness_parts = 0

        if itinerary_present:
            correctness_parts += 1

        if budget_present:
            correctness_parts += 1

        if places_present:
            correctness_parts += 1

        correctness = correctness_parts / 3


        # -------------------------------------------------
        # Relevance
        # -------------------------------------------------

        if response.strip():
            relevance = 1.0
        else:
            relevance = 0.0


        # -------------------------------------------------
        # Completeness
        # -------------------------------------------------

        matched_items = 0

        for item in expected:

            item_lower = item.lower()

            keywords = []

            if "3-day" in item_lower or "3 day" in item_lower:

                keywords.extend(
                    [
                        "day 1",
                        "day 2",
                        "day 3",
                    ]
                )

            elif "4-day" in item_lower or "4 day" in item_lower:

                keywords.extend(
                    [
                        "day 1",
                        "day 2",
                        "day 3",
                        "day 4",
                    ]
                )

            elif "5-day" in item_lower or "5 day" in item_lower:

                keywords.extend(
                    [
                        "day 1",
                        "day 2",
                        "day 3",
                        "day 4",
                        "day 5",
                    ]
                )

            elif "2-day" in item_lower or "2 day" in item_lower:

                keywords.extend(
                    [
                        "day 1",
                        "day 2",
                    ]
                )

            elif "historical" in item_lower:

                keywords.extend(
                    [
                        "historical",
                        "history",
                        "fort",
                        "palace",
                        "monument",
                    ]
                )

            elif "food" in item_lower:

                keywords.extend(
                    [
                        "food",
                        "local food",
                        "traditional",
                        "cuisine",
                        "restaurant",
                        "street food",
                    ]
                )

            elif "budget" in item_lower:

                keywords.extend(
                    [
                        "budget",
                        "₹",
                        "estimated total",
                        "accommodation",
                        "food",
                        "transport",
                    ]
                )

            elif "shopping" in item_lower:

                keywords.extend(
                    [
                        "shopping",
                        "market",
                        "bazaar",
                    ]
                )

            elif "museum" in item_lower:

                keywords.extend(
                    [
                        "museum",
                    ]
                )

            elif "monument" in item_lower:

                keywords.extend(
                    [
                        "monument",
                        "fort",
                        "palace",
                        "historical",
                    ]
                )

            elif "architecture" in item_lower:

                keywords.extend(
                    [
                        "architecture",
                        "architectural",
                        "fort",
                        "palace",
                    ]
                )

            elif "affordable" in item_lower:

                keywords.extend(
                    [
                        "affordable",
                        "budget",
                        "cheap",
                        "low-cost",
                    ]
                )

            elif "insufficient" in item_lower:

                keywords.extend(
                    [
                        "insufficient",
                        "not enough",
                        "may not be enough",
                        "tight budget",
                    ]
                )

            elif "missing" in item_lower:

                keywords.extend(
                    [
                        "missing",
                        "not provided",
                        "not specified",
                    ]
                )

            elif "ask" in item_lower:

                keywords.extend(
                    [
                        "please provide",
                        "let me know",
                        "could you provide",
                        "what is your",
                    ]
                )

            elif "assumption" in item_lower:

                keywords.extend(
                    [
                        "assumption",
                        "assuming",
                        "assume",
                    ]
                )

            else:

                words = [
                    word
                    for word in item_lower.split()
                    if len(word) > 4
                ]

                keywords.extend(words[:5])


            if keywords:

                if contains_any(
                    response_lower,
                    keywords
                ):
                    matched_items += 1


        if expected:

            completeness = min(
                matched_items / len(expected),
                1.0
            )

        else:

            completeness = 0.0


    return {
        "correctness": round(
            correctness,
            2
        ),
        "relevance": round(
            relevance,
            2
        ),
        "completeness": round(
            completeness,
            2
        ),
        "tool_usage": round(
            tool_usage,
            2
        ),
    }


# =========================================================
# CHECK WHETHER ERROR IS TEMPORARY / RETRYABLE
# =========================================================

def is_retryable_error(error):
    """
    Detect temporary Gemini/API errors.

    Retry when:
    - HTTP 503
    - UNAVAILABLE
    - 429 / RESOURCE_EXHAUSTED
    """

    error_text = str(error).upper()

    retryable_messages = [
        "503",
        "UNAVAILABLE",
        "429",
        "RESOURCE_EXHAUSTED",
        "TOO MANY REQUESTS",
        "HIGH DEMAND",
    ]

    return any(
        message in error_text
        for message in retryable_messages
    )


# =========================================================
# ACTUAL ADK AGENT EXECUTION
# =========================================================

async def run_agent(
    user_input,
    runner,
    session_service
):
    """
    Run the Travel Planner Agent using Google ADK Runner.
    """

    session = await session_service.create_session(
        app_name="travel_planner_evaluation",
        user_id="evaluation_user",
    )


    content = types.Content(
        role="user",
        parts=[
            types.Part(
                text=user_input
            )
        ],
    )


    response_parts = []


    async for event in runner.run_async(
        user_id="evaluation_user",
        session_id=session.id,
        new_message=content,
    ):

        if event.content:

            for part in event.content.parts:

                if part.text:

                    response_parts.append(
                        part.text
                    )


    response = "\n".join(
        response_parts
    ).strip()


    if not response:

        response = (
            "The agent did not return a text response."
        )


    return response


# =========================================================
# AGENT EXECUTION WITH RETRY
# =========================================================

async def generate_agent_response(
    user_input,
    runner,
    session_service,
    max_attempts=3
):
    """
    Run the agent with retry support for temporary
    Gemini/API failures.

    Maximum attempts = 3.
    """

    for attempt in range(
        1,
        max_attempts + 1
    ):

        try:

            print(
                f"\nAttempt {attempt}/{max_attempts}"
            )

            response = await run_agent(
                user_input,
                runner,
                session_service
            )

            return response


        except Exception as error:

            print(
                f"\nAttempt {attempt} failed:"
            )

            print(
                f"{type(error).__name__}: {error}"
            )


            # -------------------------------------------------
            # Retry only temporary API errors
            # -------------------------------------------------

            if (
                is_retryable_error(error)
                and attempt < max_attempts
            ):

                wait_seconds = 2 * attempt

                print(
                    f"\nTemporary API error detected."
                )

                print(
                    f"Retrying after "
                    f"{wait_seconds} seconds..."
                )

                await asyncio.sleep(
                    wait_seconds
                )

                continue


            # -------------------------------------------------
            # Permanent error or retries exhausted
            # -------------------------------------------------

            raise


# =========================================================
# MAIN ASYNC EVALUATION
# =========================================================

async def main():

    results = []


    print("=" * 60)

    print(
        "PERSONAL TRAVEL PLANNER - EVALUATION"
    )

    print("=" * 60)


    print(
        f"\nTotal test cases: "
        f"{len(test_cases)}"
    )

    print(
        f"Dataset: "
        f"{DATASET_FILE}"
    )

    print(
        f"Results: "
        f"{RESULTS_FILE}"
    )


    # =====================================================
    # CREATE ONE SESSION SERVICE
    # =====================================================

    session_service = InMemorySessionService()


    # =====================================================
    # CREATE ONE RUNNER
    # =====================================================

    runner = Runner(
        agent=root_agent,
        app_name="travel_planner_evaluation",
        session_service=session_service,
    )


    # =====================================================
    # RUN ALL TEST CASES
    # =====================================================

    for test_case in test_cases:

        test_id = test_case[
            "test_case_id"
        ]

        user_input = test_case[
            "input"
        ]


        print("\n" + "-" * 60)

        print(
            f"Running {test_id}"
        )

        print(
            f"Input: {user_input}"
        )

        print("-" * 60)


        try:

            # -------------------------------------------------
            # Generate actual agent response
            # -------------------------------------------------

            response = await generate_agent_response(
                user_input,
                runner,
                session_service,
                max_attempts=3
            )


            # -------------------------------------------------
            # Evaluate response
            # -------------------------------------------------

            scores = evaluate_response(
                test_case,
                response
            )


            # -------------------------------------------------
            # Overall score
            # -------------------------------------------------

            overall_score = (
                scores["correctness"]
                + scores["relevance"]
                + scores["completeness"]
                + scores["tool_usage"]
            ) / 4


            # -------------------------------------------------
            # PASS / FAIL
            # -------------------------------------------------

            if overall_score >= 0.70:

                status = "PASS"

            else:

                status = "FAIL"


            # -------------------------------------------------
            # Save result
            # -------------------------------------------------

            result = {

                "test_case_id":
                    test_id,

                "category":
                    test_case.get(
                        "category",
                        ""
                    ),

                "input":
                    user_input,

                "expected_behavior":
                    test_case[
                        "expected_behavior"
                    ],

                "actual_response":
                    response,

                "correctness":
                    scores[
                        "correctness"
                    ],

                "relevance":
                    scores[
                        "relevance"
                    ],

                "completeness":
                    scores[
                        "completeness"
                    ],

                "tool_usage":
                    scores[
                        "tool_usage"
                    ],

                "overall_score":
                    round(
                        overall_score,
                        2
                    ),

                "overall_percentage":
                    round(
                        overall_score * 100,
                        2
                    ),

                "status":
                    status,
            }


            results.append(
                result
            )


            # -------------------------------------------------
            # Print response
            # -------------------------------------------------

            print(
                "\nAGENT RESPONSE:"
            )

            print(
                response
            )


            # -------------------------------------------------
            # Print scores
            # -------------------------------------------------

            print(
                "\nSCORES:"
            )

            print(
                f"Correctness : "
                f"{scores['correctness']}"
            )

            print(
                f"Relevance   : "
                f"{scores['relevance']}"
            )

            print(
                f"Completeness: "
                f"{scores['completeness']}"
            )

            print(
                f"Tool Usage  : "
                f"{scores['tool_usage']}"
            )

            print(
                f"Overall     : "
                f"{round(overall_score * 100, 2)}%"
            )

            print(
                f"Status      : "
                f"{status}"
            )


        except Exception as error:

            # -------------------------------------------------
            # Handle failed execution
            # -------------------------------------------------

            error_message = (
                f"{type(error).__name__}: "
                f"{str(error)}"
            )


            print(
                "\nFINAL ERROR AFTER RETRIES:"
            )

            print(
                error_message
            )


            result = {

                "test_case_id":
                    test_id,

                "category":
                    test_case.get(
                        "category",
                        ""
                    ),

                "input":
                    user_input,

                "expected_behavior":
                    test_case[
                        "expected_behavior"
                    ],

                "actual_response":
                    "",

                "error":
                    error_message,

                "correctness":
                    0.0,

                "relevance":
                    0.0,

                "completeness":
                    0.0,

                "tool_usage":
                    0.0,

                "overall_score":
                    0.0,

                "overall_percentage":
                    0.0,

                "status":
                    "ERROR",
            }


            results.append(
                result
            )


    # =====================================================
    # CALCULATE OVERALL SCORE
    # =====================================================

    if results:

        overall_score = sum(
            result[
                "overall_score"
            ]
            for result in results
        ) / len(results)

    else:

        overall_score = 0.0


    # =====================================================
    # COUNT RESULTS
    # =====================================================

    passed = sum(
        1
        for result in results
        if result["status"] == "PASS"
    )


    failed = sum(
        1
        for result in results
        if result["status"] == "FAIL"
    )


    errors = sum(
        1
        for result in results
        if result["status"] == "ERROR"
    )


    # =====================================================
    # FAILED TEST CASES
    # =====================================================

    failed_test_cases = []


    for result in results:

        if result["status"] in [
            "FAIL",
            "ERROR"
        ]:

            failed_test_cases.append(
                {
                    "test_case_id":
                        result[
                            "test_case_id"
                        ],

                    "status":
                        result[
                            "status"
                        ],

                    "overall_percentage":
                        result[
                            "overall_percentage"
                        ],
                }
            )


    # =====================================================
    # FINAL OUTPUT
    # =====================================================

    output = {

        "evaluation_summary": {

            "total_test_cases":
                len(results),

            "passed":
                passed,

            "failed":
                failed,

            "errors":
                errors,

            "overall_score":
                round(
                    overall_score,
                    2
                ),

            "overall_percentage":
                round(
                    overall_score * 100,
                    2
                ),

            "metrics":
                [
                    "correctness",
                    "relevance",
                    "completeness",
                    "tool_usage",
                ],

            "tool_usage_note":
                (
                    "The current Travel Planner Agent "
                    "does not use external tools, so "
                    "Tool Usage is scored as 0.0."
                ),
        },

        "failed_test_cases":
            failed_test_cases,

        "results":
            results,
    }


    # =====================================================
    # SAVE RESULTS JSON
    # =====================================================

    with open(
        RESULTS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output,
            file,
            indent=2,
            ensure_ascii=False
        )


    # =====================================================
    # FINAL TERMINAL OUTPUT
    # =====================================================

    print("\n" + "=" * 60)

    print(
        "EVALUATION COMPLETED"
    )

    print("=" * 60)

    print(
        f"Total Test Cases : "
        f"{len(results)}"
    )

    print(
        f"Passed           : "
        f"{passed}"
    )

    print(
        f"Failed           : "
        f"{failed}"
    )

    print(
        f"Errors           : "
        f"{errors}"
    )

    print(
        f"Overall Score    : "
        f"{round(overall_score * 100, 2)}%"
    )

    print("=" * 60)

    print(
        "\nResults saved to:"
    )

    print(
        RESULTS_FILE
    )


# =========================================================
# PROGRAM ENTRY POINT
# =========================================================

if __name__ == "__main__":

    asyncio.run(
        main()
    )