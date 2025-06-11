# ArVoice Diacritization Challenge - Starting Kit

This starting kit provides a basic example of the submission format.

## Submission Requirements

Participants must submit a **ZIP archive** containing a single text file named `prediction.txt`.

-   The `prediction.txt` file must be **UTF-8 encoded**.
-   It should contain your system's diacritized output corresponding to the test data provided by the evaluation system.

## Contents of this Kit
-   `baseline.py`: Contains the implementation of the baseline model used for initial predictions.
-   `calculate_der.py`: Evaluates the model performance.
-   `dataprocess.py`:   Handles post-processing of the `predictions.txt` file to prepare final results.
-   `prediction.txt`: An example of a diacritized text file. You should replace its contents with your model's output on the official test set.
-   `README.md` (this file)

## How to Submit

1.  Generate your `prediction.txt` file using your diacritization system on the input data provided during the evaluation run.
2.  Ensure the file is UTF-8 encoded.
3.  Create a ZIP archive containing **only** your `prediction.txt` file.
    Example (Linux/macOS):
    ```bash
    zip submission.zip prediction.txt
    ```
4.  Upload `submission.zip` to the Codabench platform.

Good luck! 