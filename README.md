# ResQTrack - Animal Rescue Coordination Platform

ResQTrack is a comprehensive animal rescue coordination platform built with Flask, HTML, CSS, and JavaScript. It uses CSV files as a database through Pandas and integrates with the OpenStreetMap API to locate veterinary hospitals.

## Features

- **Report Animal Emergencies**: Users can report injured or distressed animals with detailed information
- **Donate to Rescue Efforts**: Support rescue operations through monetary donations
- **Find Veterinary Hospitals**: Locate nearby veterinary hospitals using OpenStreetMap API
- **Admin Dashboard**: Manage cases, donations, and hospitals without login
- **Responsive Design**: Works on both desktop and mobile devices

## Tech Stack

- **Backend**: Python, Flask, Pandas
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Database**: CSV files managed with Pandas
- **APIs**: OpenStreetMap Nominatim API

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd resqtrack
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python app.py
   ```

4. Open your browser and go to `http://localhost:5000`

## Usage

### User Interface

- **Homepage**: Access all features from the main page
- **Report Case**: Report an animal emergency with location and details
- **Donate**: Make monetary donations to support rescue efforts
- **Hospitals**: Search for veterinary hospitals in any city
- **Admin Panel**: Access all data management features at `/admin`

### Admin Features

The admin panel (`/admin`) provides access to:
- View and manage all reported cases
- Track donations and total amounts collected
- Manage registered veterinary hospitals
- Search for new hospitals using the API
- Update case statuses

**Note**: There is no login required for the admin panel - it's accessible directly.

## Project Structure

```
resqtrack/
│── app.py                 # Main Flask application
│── requirements.txt       # Python dependencies
│── extensions/
│     └── csv_manager.py   # CSV database management
│── routes/
│     ├── cases.py         # Case reporting routes
│     ├── donations.py     # Donation routes
│     ├── hospitals.py     # Hospital search and management
│     ├── admin.py         # Admin dashboard routes
│     └── common.py        # Common routes (homepage, etc.)
│── database/
│     ├── cases.csv        # Reported cases
│     ├── donations.csv    # Donation records
│     ├── hospitals.csv    # Registered hospitals
│     └── emergency.csv    # Emergency response data
│── static/
│     ├── css/
│     │     └── styles.css # Custom styling
│     ├── js/
│     │     ├── main.js    # Main JavaScript functions
│     │     └── admin.js   # Admin-specific JavaScript
│     └── uploads/         # Uploaded media files
│── templates/
      ├── index.html       # Homepage
      ├── report_case.html # Case reporting form
      ├── donate.html      # Donation form
      ├── hospitals.html   # Hospital search page
      └── admin.html       # Admin dashboard
```

## API Endpoints

### Cases
- `POST /cases/report` - Report a new case
- `GET /cases/all` - Get all cases
- `POST /cases/update-status` - Update case status

### Donations
- `POST /donations/add` - Record a new donation
- `GET /donations/all` - Get all donations

### Hospitals
- `GET /hospitals/search?city=<city>` - Search hospitals in a city
- `POST /hospitals/add` - Add a new hospital
- `GET /hospitals/all` - Get all hospitals

### Admin
- `GET /admin` - Admin dashboard
- `GET /admin/stats` - Get statistics
- `GET /admin/api/<table>` - Get all records from a table
- `POST /admin/api/<table>` - Add/delete records

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License.