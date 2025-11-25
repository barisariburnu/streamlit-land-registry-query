# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial open source release
- Comprehensive README with installation and usage instructions
- Contributing guidelines
- MIT License
- Docker and Docker Compose support
- Environment configuration examples

## [1.0.0] - 2024-11-25

### Added
- Hierarchical land registry search functionality
- Support for Province, District, Neighborhood, Block, and Parcel filtering
- Share information display with owner details
- Interactive visualizations:
  - Pie chart for share distribution
  - Bar chart for comparative view
  - Waterfall chart for cumulative distribution
- Summary statistics dashboard
- Export functionality:
  - CSV export with UTF-8 encoding
  - Formatted Excel export
- Database connection pooling
- Automatic retry logic for database operations
- Caching for improved performance
- Error handling and logging
- Responsive UI with Streamlit
- Dark theme support
- Docker containerization

### Technical Features
- PostgreSQL database integration via SQLAlchemy 2.0
- Connection health checks and automatic reconnection
- Exponential backoff for failed operations
- Type hints throughout the codebase
- Comprehensive error handling
- Efficient data processing with Pandas
- Interactive charts with Plotly

[Unreleased]: https://github.com/barisariburnu/streamlit-land-registry-query/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/barisariburnu/streamlit-land-registry-query/releases/tag/v1.0.0
