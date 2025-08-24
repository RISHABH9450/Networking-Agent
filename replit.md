# Overview

The Networking Troubleshooter Agent is a comprehensive web application designed to diagnose and troubleshoot networking issues for domains and IP addresses. The application performs multiple diagnostic checks including DNS resolution, SSL certificate validation, HTTP connectivity, ping tests, and GeoIP lookups. It provides both beginner-friendly and expert-level explanations of results, along with health scoring and fix suggestions.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Backend Architecture
The application uses a Flask-based web server with a modular diagnostic system. The core architecture follows a service-oriented pattern where each diagnostic function is isolated in its own module within the `diagnostics` package. The main `agent.py` serves as the orchestrator that coordinates all diagnostic checks and aggregates results.

**Key Components:**
- **Flask Web Framework**: Provides HTTP endpoints and template rendering
- **Diagnostic Modules**: Separate modules for DNS, SSL, HTTP, ping, and GeoIP checks
- **Configuration Management**: Centralized settings using Pydantic for environment variable handling
- **Explanation System**: Dual-mode explanations (beginner/expert) in the `utils` package

## Frontend Architecture
The frontend uses server-side rendering with Jinja2 templates and Bootstrap for styling. The interface is designed with a dark theme optimized for technical users. The application provides both web interface and API endpoints for programmatic access.

**Template Structure:**
- **Base Template**: Provides common layout, navigation, and Bootstrap integration
- **Index Template**: Main diagnostic form with target input and mode selection
- **Results Template**: Comprehensive results display with health scores and explanations

## Data Flow Architecture
The application follows a request-response pattern where user input triggers a comprehensive diagnostic pipeline. Each diagnostic module returns standardized result dictionaries that are then processed through explanation layers before being presented to the user.

**Processing Pipeline:**
1. Input normalization and validation
2. Parallel execution of diagnostic checks
3. Result aggregation and health score calculation
4. Mode-specific explanation generation
5. Template rendering with formatted results

## Error Handling Strategy
Each diagnostic module implements defensive programming with try-catch blocks that return structured error information. This ensures that failures in one diagnostic check don't prevent other checks from completing, providing partial results even when some services are unavailable.

# External Dependencies

## Core Web Framework
- **Flask**: Primary web framework for HTTP handling and template rendering
- **Werkzeug**: WSGI utilities and request processing middleware

## HTTP and Network Libraries
- **httpx**: Modern HTTP client for web connectivity checks with timeout and redirect handling
- **ping3**: ICMP ping implementation for network reachability testing
- **socket**: Built-in Python library for low-level network operations

## Configuration and Validation
- **Pydantic**: Data validation and settings management with environment variable integration
- **python-dotenv**: Environment variable loading from .env files

## SSL and Security
- **ssl**: Built-in Python SSL library for certificate validation and security checks

## Third-Party Services
- **ipapi.co**: Free GeoIP service for location and ISP information lookup
- **DNS System**: Standard DNS resolution using system resolvers

## Frontend Dependencies
- **Bootstrap 5.3**: CSS framework with dark theme support
- **Bootstrap Icons**: Icon library for user interface elements
- **Jinja2**: Template engine for server-side rendering

## Optional Integrations
- **Redis**: Configured for caching diagnostic results (optional, not actively used)
- **Portia API**: Fully integrated AI-powered diagnostic insights with root cause analysis, intelligent recommendations, performance scoring, and predictive insights

The application is designed to be resilient to external service failures, with graceful degradation when third-party services are unavailable.