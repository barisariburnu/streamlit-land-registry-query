# Land Registry Query System

A web application for querying, visualizing, and exporting land registry and share information stored in a PostgreSQL database.

## Features

- Hierarchical search by:
  - Province
  - District
  - Neighborhood
  - Block
  - Parcel
- Detailed share information display
- Visual analytics:
  - Pie chart for share distribution
  - Bar chart for comparative view
  - Waterfall chart for cumulative distribution
- Summary statistics
- Export options:
  - CSV format
  - Formatted Excel spreadsheets

## Technical Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.8+
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy 2.0
- **Visualization**: Plotly
- **Data Processing**: Pandas

## Installation

1. Install Python 3.8 or higher

2. Clone the repository:
```bash
git clone https://github.com/yourusername/streamlit-land-registry-query.git
cd streamlit-land-registry-query
```

3. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
```

4. Install requirements:
```bash
pip install -r requirements.txt
```

## Configuration

1. Create `.streamlit` directory:
```bash
mkdir .streamlit
```

2. Create `.streamlit/secrets.toml`:
```toml
[postgres]
host = "database_host"
port = "5432"
database = "database_name"
user = "username"
password = "password"
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Visit the provided URL in your browser (typically http://localhost:8501)

3. To perform a search:
   - Select a Province
   - Select a District
   - Select a Neighborhood
   - Select a Block number
   - Select a Parcel number
   - Click "Search"

4. View results:
   - Detailed information in tabular format
   - Visual representations
   - Summary statistics

5. Export results:
   - Download as CSV
   - Download as formatted Excel

## Project Structure

```
streamlit-land-registry-query/
├── .gitignore
├── .streamlit/
│   ├── config.toml        # Streamlit settings
│   └── secrets.toml       # Secret configuration
├── app.py                 # Main application
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Key Notes

- Application is optimized for dark mode
- All search fields are mandatory
- Excel exports include automatic formatting
- Full UTF-8 encoding support for special characters
- Cached database queries for better performance

## Security Features

- SQL Injection protection through SQLAlchemy
- Parameter validation
- Secure database connections
- Sensitive information stored in secrets.toml
- Type checking and input validation

## Database Models

The application uses two main models:

### Land Registry (Zemin)
```python
class Zemin:
    - ID (Primary Key)
    - ParcelRef
    - Province
    - District
    - Neighborhood
    - Block
    - Parcel
```

### Share Information (ZeminHisse)
```python
class ZeminHisse:
    - ID (Primary Key)
    - LandRegistryRef (Foreign Key)
    - FirstName
    - LastName
    - FatherName
    - NationalID
    - ShareNumerator
    - ShareDenominator
```

## Troubleshooting

Common issues and solutions:

1. Database Connection Errors:
   - Verify PostgreSQL service is running
   - Check connection credentials
   - Confirm database permissions

2. Chart Generation Errors:
   - Verify data format consistency
   - Check for null values
   - Ensure proper numeric type conversion

3. Export Errors:
   - Check disk space
   - Verify write permissions
   - Ensure proper encoding settings

## Performance Considerations

- Database queries are cached using Streamlit's caching
- Lazy loading for dropdown options
- Optimized SQL queries with proper indexing
- Efficient data processing with Pandas

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Push to the branch
5. Create a Pull Request

Guidelines:
- Follow PEP 8 style guide
- Add tests for new features
- Update documentation
- Use type hints
- Handle errors gracefully

## Testing

Run tests using:
```bash
pytest tests/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support:
1. Check the issues section
2. Review the troubleshooting guide
3. Contact the development team

## Future Improvements

- Add user authentication
- Implement bulk export
- Add more visualization options
- Create API endpoints
- Add map integration

## Acknowledgments

- Streamlit team for the amazing framework
- SQLAlchemy team for the robust ORM
- Plotly team for the visualization library