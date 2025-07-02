# Contributing to Telegram Link Collector Bot

Thank you for your interest in contributing to the Telegram Link Collector Bot! This document provides guidelines and instructions for contributing.

## Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/telegram_bot.git
   cd telegram_bot
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your test bot token
   ```

## Code Style

We follow PEP 8 guidelines with these specifics:

- Use 4 spaces for indentation
- Maximum line length: 88 characters
- Use descriptive variable names
- Add docstrings to all classes and methods
- Keep functions focused and small
- Use type hints where possible

## Testing

- Write tests for new features
- Ensure all tests pass before submitting
- Include both unit and integration tests
- Test error cases and edge conditions

## Pull Request Process

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Write clean, documented code
   - Follow code style guidelines
   - Add tests for new features

3. **Commit Changes**
   - Use clear commit messages
   - Reference issues if applicable
   ```bash
   git commit -m "Add feature: description (#issue)"
   ```

4. **Submit Pull Request**
   - Provide clear description
   - Link related issues
   - List any breaking changes
   - Update documentation

## Code Review

- All submissions require review
- Address review feedback promptly
- Keep discussions professional
- Be open to suggestions

## Documentation

Update documentation for:
- New features
- Changed functionality
- Configuration changes
- New dependencies

## Issue Reporting

When reporting issues:
1. Use issue templates
2. Provide clear reproduction steps
3. Include relevant logs
4. Specify your environment

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License. 