# Contributing to Land Registry Query System

First off, thank you for considering contributing to the Land Registry Query System! It's people like you that make this project such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our commitment to providing a welcoming and inspiring community for all. Please be respectful and constructive in your communications.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps to reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed and what behavior you expected**
* **Include screenshots if applicable**
* **Include your environment details** (OS, Python version, Docker version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a detailed description of the suggested enhancement**
* **Explain why this enhancement would be useful**
* **List any alternative solutions you've considered**

### Pull Requests

Please follow these steps:

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following our coding standards
3. **Test your changes** thoroughly
4. **Update documentation** as needed
5. **Commit your changes** with clear, descriptive messages
6. **Push to your fork** and submit a pull request

#### Pull Request Guidelines

* Follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python code
* Use type hints for function parameters and return values
* Add docstrings to all functions and classes
* Keep functions focused and modular
* Handle errors gracefully with appropriate error messages
* Update the README.md if you change functionality
* Add your changes to CHANGELOG.md under "Unreleased"

#### Code Style

```python
# Good example
def calculate_share_area(numerator: int, denominator: int, total_area: float) -> float:
    """
    Calculate the area corresponding to a share fraction.
    
    Args:
        numerator: Share numerator
        denominator: Share denominator
        total_area: Total area in square meters
        
    Returns:
        Area corresponding to the share in square meters
        
    Raises:
        ValueError: If denominator is zero
    """
    if denominator == 0:
        raise ValueError("Denominator cannot be zero")
    return (numerator / denominator) * total_area
```

### Development Setup

1. Clone your fork:
```bash
git clone https://github.com/YOUR_USERNAME/streamlit-land-registry-query.git
cd streamlit-land-registry-query
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure your database:
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit .streamlit/secrets.toml with your database credentials
```

5. Run the application:
```bash
streamlit run app.py
```

### Testing

Before submitting a pull request, make sure:

* Your code runs without errors
* Database queries work correctly
* Visualizations render properly
* Export functions generate valid files
* Error handling works as expected

### Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests after the first line

Examples:
```
Add waterfall chart visualization

Add support for visualizing cumulative share distribution
using waterfall charts. Closes #123
```

### Documentation

* Update README.md for any user-facing changes
* Add docstrings to all new functions and classes
* Comment complex logic
* Update CHANGELOG.md

## Project Structure

```
streamlit-land-registry-query/
├── .streamlit/           # Streamlit configuration
│   ├── config.toml      # App configuration
│   └── secrets.toml     # Database credentials (not in git)
├── app.py               # Main application
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker image definition
├── docker-compose.yml  # Docker Compose configuration
└── README.md           # Project documentation
```

## Questions?

Feel free to open an issue with your question or reach out to the maintainers:

* GitHub: [@barisariburnu](https://github.com/barisariburnu)

Thank you for contributing! 🎉
