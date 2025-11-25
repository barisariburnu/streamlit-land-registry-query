# Land Registry Query System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B.svg)](https://streamlit.io)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-336791.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)

A modern, responsive web application for querying, visualizing, and exporting land registry and share information from PostgreSQL databases. Built with Streamlit for an intuitive user experience.

## ✨ Features

### 🔍 Advanced Search
- **Hierarchical filtering** by Province → District → Neighborhood → Block → Parcel
- **Smart cascading dropdowns** with dynamic data loading
- **Cached queries** for optimal performance

### 📊 Rich Visualizations
- **Pie Chart** - Share distribution overview
- **Bar Chart** - Comparative shareholder analysis
- **Waterfall Chart** - Cumulative area distribution
- **Interactive charts** powered by Plotly

### 📈 Analytics
- Real-time summary statistics
- Shareholder count and metrics
- Area calculations with precision

### 💾 Export Options
- **CSV** export with UTF-8 encoding (Turkish character support)
- **Excel** export with formatted spreadsheets
- Customizable file naming

### 🔧 Technical Features
- **Connection pooling** for database efficiency
- **Automatic retry logic** with exponential backoff
- **Health checks** and automatic reconnection
- **Comprehensive error handling** and logging
- **Responsive UI** with dark theme
- **Docker support** for easy deployment
- **Internationalization** support (Turkish/English)

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone the repository**
```bash
git clone https://github.com/barisariburnu/streamlit-land-registry-query.git
cd streamlit-land-registry-query
```

2. **Configure database connection**
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Edit `.streamlit/secrets.toml` with your PostgreSQL credentials:
```toml
[postgres]
host = "your_database_host"
port = 5432
database = "your_database_name"
user = "your_username"
password = "your_password"
```

3. **Run with Docker Compose**
```bash
docker-compose up -d --build
```

4. **Access the application**
Open your browser and navigate to `http://localhost:8502`

### Manual Installation

1. **Prerequisites**
   - Python 3.10 or higher
   - PostgreSQL 13 or higher
   - pip package manager

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure database**
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit .streamlit/secrets.toml with your credentials
```

4. **Run the application**
```bash
streamlit run app.py
```

## 📋 Database Schema

The application expects the following PostgreSQL schema:

### `zemin` Table (Land Registry)
```sql
CREATE TABLE zemin (
    "ID" SERIAL PRIMARY KEY,
    "ParselRef" VARCHAR(255),
    "Il" VARCHAR(100),           -- Province
    "Ilce" VARCHAR(100),          -- District
    "MahalleKoyAdi" VARCHAR(100), -- Neighborhood
    "Ada" VARCHAR(50),            -- Block
    "Parsel" VARCHAR(50),         -- Parcel
    "Yuzolcum" DECIMAL(15,2)      -- Area in square meters
);
```

### `zeminhisse` Table (Share Information)
```sql
CREATE TABLE zeminhisse (
    "ID" SERIAL PRIMARY KEY,
    "ZeminRef" INTEGER REFERENCES zemin("ID"),
    "Adi" VARCHAR(100),           -- First name
    "Soyadi" VARCHAR(100),        -- Last name
    "BabaAdi" VARCHAR(100),       -- Father's name
    "TCKimlikNo" VARCHAR(11),     -- National ID
    "HissePay" INTEGER,           -- Share numerator
    "HissePayda" INTEGER          -- Share denominator
);
```

**Recommended Indexes:**
```sql
CREATE INDEX idx_zemin_location ON zemin("Il", "Ilce", "MahalleKoyAdi", "Ada", "Parsel");
CREATE INDEX idx_zeminhisse_ref ON zeminhisse("ZeminRef");
```

## ⚙️ Configuration

### Language Settings

Edit `config.py` to change the application language:

```python
# Change to "en" for English
APP_LANGUAGE = "tr"  # Default: Turkish
```

### Streamlit Configuration

Customize appearance in `.streamlit/config.toml`:
- Theme colors
- Server settings
- UI behavior

### Application Settings

The app includes several configurable parameters in `app.py`:

```python
# Database connection pool
pool_size=5
max_overflow=10
pool_timeout=30
pool_recycle=1800

# Cache TTL
@st.cache_data(ttl=300)  # 5 minutes

# Retry logic
max_retries=3
delay_seconds=1
```

##  🐳 Docker Deployment

### Production Deployment

1. **Configure firewall** (if needed)
```bash
# For CentOS/RHEL
sudo firewall-cmd --permanent --add-port=8502/tcp
sudo firewall-cmd --reload

# For Ubuntu/Debian
sudo ufw allow 8502/tcp
```

2. **Run in production**
```bash
docker-compose up -d
```

3. **View logs**
```bash
docker-compose logs -f
```

4. **Update application**
```bash
docker-compose down
git pull
docker-compose up -d --build
```

### Docker Commands Reference

```bash
# Stop the application
docker-compose down

# Restart the application
docker-compose restart

# View container status
docker-compose ps

# Access container shell
docker-compose exec streamlit-land-registry-query sh
```

## 📊 Usage Guide

1. **Select Location**
   - Choose a Province from the dropdown
   - Select a District (filtered by Province)
   - Choose a Neighborhood (filtered by District)
   - Select a Block number (filtered by Neighborhood)
   - Choose a Parcel number (filtered by Block)

2. **Search**
   - Click the "Search" button
   - Results will display in a table below

3. **Analyze**
   - View interactive charts in the Visualizations section
   - Check summary statistics for quick insights

4. **Export**
   - Download results as CSV for spreadsheet applications
   - Download as Excel for formatted reports

## 🔧 Development

### Project Structure

```
streamlit-land-registry-query/
├── .streamlit/
│   ├── config.toml              # Streamlit configuration
│   └── secrets.toml.example     # Database credentials template
├── app.py                       # Main application
├── config.py                    # Language and labels configuration
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker image definition
├── docker-compose.yml           # Docker Compose configuration
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── LICENSE                      # MIT License
├── README.md                    # This file
├── CONTRIBUTING.md  # Contribution guidelines
└── CHANGELOG.md                 # Version history
```

### Adding Features

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 🐛 Troubleshooting

### Database Connection Issues
- Verify PostgreSQL is running
- Check credentials in `secrets.toml`
- Ensure database user has SELECT permissions
- Check network connectivity and firewall rules

### Chart Rendering Issues
- Verify data contains numeric values
- Check for NULL values in the database
- Ensure proper data type conversion

### Performance Issues
- Add database indexes (see Database Schema section)
- Adjust cache TTL in `app.py`
- Increase database connection pool size
- Consider database query optimization

### Docker Issues
- Ensure Docker daemon is running
- Check port 8502 is not in use
- Verify docker-compose.yml configuration
- Check container logs with `docker-compose logs`

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Baris Ariburnu**
- GitHub: [@barisariburnu](https://github.com/barisariburnu)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!

## 📜 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## 🔮 Roadmap

- [ ] User authentication and authorization
- [ ] Multi-user support with role-based access
- [ ] Bulk export functionality with batch processing
- [ ] Additional chart types (heatmaps, treemaps)
- [ ] RESTful API endpoints
- [ ] Map integration for geographical visualization
- [ ] PDF report generation
- [ ] Advanced search filters
- [ ] Data caching improvements
- [ ] Mobile-responsive design enhancements

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io) - Amazing framework for data apps
- [SQLAlchemy](https://www.sqlalchemy.org/) - Robust database toolkit
- [Plotly](https://plotly.com/) - Interactive visualization library
- [Pandas](https://pandas.pydata.org/) - Data manipulation library

---

**Note:** This is a data querying and visualization tool. Ensure you have proper authorization to access and display land registry information in compliance with your local regulations and privacy laws.