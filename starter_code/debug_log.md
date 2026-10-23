# Debug log (Part A)

Name: Fahad Hussain  Date: October 21st, 2026

Fill one block per ticket, in the order you fixed them. Use the method from the lesson: Reproduce, Read,
Isolate, Hypothesise, Test, Fix, Verify. Short answers are fine, but the EVIDENCE line must be something
you actually saw (a pdb command and its output, or a print line).

## BUG-1
- Symptom (what I saw): Incorrect output (3 instead of expected 2.5)
- Family (syntax / runtime / logic): logic
- Hypothesis (before I looked): median is being calculated/returned as int instead of float
- Evidence (pdb command + output, or print output): "3" is being printed. 
- Root cause (one sentence): logic was only sound for odd-length input lists.
- Fix (one sentence): added logic for even-length input lists (return avg of middle 2 numbers)
- Verified by: Running run_report.py and ensuring new output matches expected value.

## BUG-2
- Symptom: Top 3 slowests tests returns only 2 items, 0 for 'n' returns the entire list 
- Family: Logic
- Hypothesis: There could be less than 3 inputted test cases, and '0' is not being handled explicitly in the code
- Evidence: Only 2 elements in the list being printed through run_report.py.
- Root: Incorrect slicing parameters (-1 included when not needed), n value of 0 not being handled.
- Fix: Removing the -1 and adding an if-statement to return [] if n is 0.
- Verified by: running check_exercise.py and run_report.py and comparing with expected number of results.

## BUG-3
- Symptom: Obtaining KeyError when trying to obtain counts per suite.
- Family: runtime
- Hypothesis: 'login' exists at a different depth in the dict.
- Evidence: ran pp locals() in pdb; saw result has 'suite': 'login' but grouped dict starts empty {} so grouped['login'] raises KeyError.
- Root: The nested keys for suite and status do not exist in grouped yet before trying to increment, and missing suite keys are not handled.
- Fix: Use result.get("suite", "unknown") and check if suite and status exist in grouped before incrementing their count.
- Verified by: Ran python run_report.py 3 and saw suites and statuses counted properly.

## BUG-4
- Symptom: Two different reports show the same flaky list (['t2', 't9'] for both).
- Family: logic
- Hypothesis: The default list argument is being shared between function calls.
- Evidence: Ran python run_report.py 4 and saw (['t2', 't9'], ['t2', 't9']) printed instead of independent lists.
- Root: Default argument flaky=[] is mutable and only evaluated once when the function is defined, sharing the list across calls.
- Fix: Changed default argument to flaky=None and initialized flaky = [] inside the function if flaky is None.
- Verified by: Ran python run_report.py 4 and confirmed outputs are separate (['t2'], ['t9']).

## BUG-5
- Symptom: Report id never gets created; crashes with UnboundLocalError.
- Family: runtime
- Hypothesis: Assigning to run_counter makes Python treat it as a local variable.
- Evidence: Ran python run_report.py 5 and saw UnboundLocalError: cannot access local variable 'run_counter' where it is not associated with a value.
- Root: next_run_id assigns to run_counter without declaring it global, so Python treats it as an unassigned local.
- Fix: Added global run_counter inside next_run_id().
- Verified by: Ran python run_report.py 5 and saw RUN-0001 returned.

## BUG-6
- Symptom: latest_ms shows the wrong duration (80 instead of 150) and original list gets sorted.
- Family: logic
- Hypothesis: One of the earlier functions in summarise_run changed the order of durations in place.
- Evidence: Printed durations before and after slowest() and saw the list changed from [120, 80, 340, 95, 210, 150] to [340, 210, 150, 120, 95, 80].
- Root: slowest() was calling durations.sort() which sorts in place, mutating the input list before latest_ms was retrieved with durations[-1].
- Fix: Replaced durations.sort() with sorted(durations, reverse=True) so the original list is not modified.
- Verified by: Ran python run_report.py 6 and verified latest_ms is 150 and original list order is preserved.

## BUG-7
- Symptom: Dashboard report crashes when there are no test durations recorded.
- Family: runtime
- Hypothesis: Calling median() or accessing durations[-1] fails when durations is empty.
- Evidence: Ran python run_report.py 7 and saw IndexError: list index out of range at durations[-1].
- Root: summarise_run does not guard against an empty durations list when indexing [-1] or calling median, and median([]) needs to raise ValueError.
- Fix: Raised ValueError in median() when values is empty, and guarded median_ms and latest_ms in summarise_run with conditional expressions to return None when durations is empty.
- Verified by: Ran python run_report.py 7 and saw median_ms and latest_ms were None and no crash occurred.

## Reflection (3 sentences)
BUG-6 was the hardest bug to track down because there was no crash or error message; everything executed cleanly, but the list was silently being sorted in place which broke subsequent operations. Using simple print statements before and after calling slowest() inside summarise_run helped the most to see that durations was being mutated. Next time, I will be more cautious when functions take mutable data like lists and use sorted() to return a new copy rather than modifying inputs directly.
