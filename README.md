# Tennis Court Booking Automation

This automation script helps you book tennis courts through the Chicago Park District website.

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Setup Instructions

### Step 1: Create a Virtual Environment

Create a virtual environment to isolate the project dependencies:

**On macOS/Linux:**

```bash
python3 -m venv venv
```

**On Windows:**

```bash
python -m venv venv
```

### Step 2: Activate the Virtual Environment

Activate the virtual environment before installing packages:

**On macOS/Linux:**

```bash
source venv/bin/activate
```

**On Windows:**

```bash
venv\Scripts\activate
```

After activation, you should see `(venv)` at the beginning of your command prompt.

### Step 3: Install Required Packages

Install the required packages:

```bash
pip install drissionpage pandas
```

### Step 4: Configure Your Settings

#### Option A: Configure via `times.xlsx` (Recommended)

The script reads booking preferences from `times.xlsx`. Create this file in the same directory as `automation.py` with the following structure:

| Date       | Time | BallMachine |
| ---------- | ---- | ----------- |
| 2025-12-15 | 6 AM | Yes         |
|            | 7 AM |             |
|            | 8 AM |             |

**Column Details:**

- **Date**: Your preferred booking date in YYYY-MM-DD format (e.g., "2025-12-15")
- **Time**: Preferred time slots in 12-hour format (e.g., "6 AM", "7 PM", "8:30 AM")
- **BallMachine**: Set to "Yes" or "Y" if you need a ball machine, "No" or "N" otherwise

**Note:** The script will use the first row's Date and BallMachine value, but will try all Time values listed in the file.

#### Option B: Configure via Code

You can also update the following variables directly in `automation.py`:

1. **Username** (Line 19): Update with your email address

   ```python
   USERNAME = "your-email@example.com"
   ```
2. **Password** (Line 20): Update with your account password

   ```python
   PASSWORD = "your-password"
   ```
3. **CVV Code** (Line 21): Update with your card's CVV code

   ```python
   CVV_CODE = "123"
   ```
4. **Event Name** (Line 23): Update with your event/booking name

   ```python
   EVENT_NAME = "My Tennis Booking"
   ```

### Step 5: Run the Automation Script

Run the script using:

```bash
python automation.py
```

The script will:

- Read your preferences from `times.xlsx` (date, time slots, and ball machine preference)
- Automatically log in, navigate to the booking page, and select your date and time
- Click "Confirm Bookings" button
- **Wait 10 minutes** before proceeding to the checkout page (useful if you schedule the script to run at 6:50 AM before bookings open at 7:00 AM)
- Complete the booking and payment process

**Important:** The script includes a 10-minute wait period after clicking "Confirm Bookings" and before proceeding to checkout. This is designed for scenarios where bookings open at a specific time (e.g., 7:00 AM). Schedule your script to run 10 minutes before (e.g., 6:50 AM) so it's ready when bookings open.

## Notes

- Make sure your virtual environment is activated before running the script
- The `times.xlsx` file must be in the same directory as `automation.py`
- The script will open a browser window to perform the automation
- Keep the browser window open during the automation process
- The script includes error handling and will attempt to recover from service errors automatically
- The script waits 10 minutes after clicking "Confirm Bookings" before proceeding to checkout (see above)
- Make sure your Excel file has the correct column names: "Date", "Time", and "BallMachine"

## Troubleshooting

If you encounter any issues:

- Ensure all dependencies are installed correctly (`drissionpage` and `pandas`)
- Verify that your `times.xlsx` file exists and has the correct format
- Check that your credentials (username, password, CVV) are correct in `automation.py`
- Verify the Date format in `times.xlsx` is YYYY-MM-DD (e.g., "2025-12-15")
- Ensure Time values in `times.xlsx` are in 12-hour format (e.g., "6 AM", "7 PM")
- Check that you have an active internet connection
- Make sure the virtual environment is activated
- Ensure `times.xlsx` is in the same directory as `automation.py`
