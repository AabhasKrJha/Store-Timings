
# Store Timings

### Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python 3:** You need to have Python 3 installed. You can download it from [python.org](https://www.python.org/downloads/).

### Installation

1. Create a virtual environment for your project (optional but recommended):

   ```bash
   python3 -m venv venv
   ```

2. Activate the virtual environment:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

3. Install the required Python packages using `pip`:

   ```bash
   pip install Flask Flask-SQLAlchemy pytz
   ```

### Database Setup

1. Create a directory csv_data parallel to "src" and place the csv files init by the names - "store_hours.csv", "store_status.csv" and "timezones.csv".

2. Run `convert.py` to create the SQLite database:

   ```bash
   python convert.py
   ```

### Usage

1. Start the Flask application by running `run.py`:

   ```bash
   python run.py
   ```

2. Open your web browser and go to [http://localhost:5000](http://localhost:5000) to access the application.