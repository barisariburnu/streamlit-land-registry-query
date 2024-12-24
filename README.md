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
- **Backend**: Python 3.10+
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy 2.0
- **Visualization**: Plotly
- **Data Processing**: Pandas
- **Containerization**: Docker

## Installation

1. Install Docker and Docker Compose:
```bash
# Docker repository'sini ekleyin
sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# Docker'ı yükleyin
sudo dnf install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y

# Docker'ı başlatın
sudo systemctl start docker
sudo systemctl enable docker
```

2. Clone the repository:
```bash
git clone https://github.com/barisariburnu/streamlit-land-registry-query.git
cd streamlit-land-registry-query
```

3. Configure firewall:
```bash
# Install Firewall (if not installed)
sudo dnf install firewalld -y

# Start and activate the Firewall service
sudo systemctl start firewalld
sudo systemctl enable firewalld

# Open port 8502
sudo firewall-cmd --permanent --add-port=8502/tcp
sudo firewall-cmd --reload

# Check that the port is open
sudo firewall-cmd --list-ports
```

## Configuration

1. Create `.env` file:
```env
POSTGRES_HOST=database_host
POSTGRES_PORT=5432
POSTGRES_DB=database_name
POSTGRES_USER=username
POSTGRES_PASSWORD=password
```

## Project Structure

```
streamlit-land-registry-query/
├── .gitignore
├── .env                  # Environment variables
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose configuration
├── app/                 # Application directory
│   └── main.py         # Main application
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Usage

1. Start the application with Docker:
```bash
sudo docker-compose up -d --build
```

2. Visit http://your-server-ip:8501 in your browser

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

## Docker Commands

```bash
# View logs
sudo docker-compose logs -f

# Stop application
sudo docker-compose down

# Restart application
sudo docker-compose restart

# Rebuild and start
sudo docker-compose up -d --build
```

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