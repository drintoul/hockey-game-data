# hockey
Analysis and Predictions using NHL data from https://www.hockey-reference.com

<h1>data.py</h1>
<h2>get_games</h2>
  Python function to retrieve tables from website and return as Pandas DataFrame; not all columns available for all years (e.g., Attendance was not recorded in early history); DataFrame column headings are standardized.
<h2>ml_prep</h2>
  Python function to change datatypes, filter games where attendance or game length were not recorded, and filter 'special' games like Outdoor or International games.
