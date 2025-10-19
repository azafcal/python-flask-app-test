#!/usr/bin/env python3
"""
Test runner script for the Flask Todo application.

This script provides convenient ways to run different types of tests
and generate reports.
"""

import sys
import subprocess
import argparse
import os


def run_command(cmd):
    """Run a command and return the result."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.stdout:
        print("STDOUT:", result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return result.returncode == 0


def run_unit_tests(verbose=False):
    """Run only unit tests."""
    cmd = ["uv", "run", "pytest", "-m", "unit"]
    if verbose:
        cmd.append("-v")
    return run_command(cmd)


def run_integration_tests(verbose=False):
    """Run only integration tests."""
    cmd = ["uv", "run", "pytest", "-m", "integration"]
    if verbose:
        cmd.append("-v")
    return run_command(cmd)


def run_api_tests(verbose=False):
    """Run only API tests."""
    cmd = ["uv", "run", "pytest", "-m", "api"]
    if verbose:
        cmd.append("-v")
    return run_command(cmd)


def run_slow_tests(verbose=False):
    """Run slow/performance tests."""
    cmd = ["uv", "run", "pytest", "-m", "slow"]
    if verbose:
        cmd.append("-v")
    return run_command(cmd)


def run_all_tests(verbose=False, coverage=False):
    """Run all tests."""
    cmd = ["uv", "run", "pytest"]
    
    if coverage:
        cmd.extend(["--cov=src/flask_todo_app", "--cov-report=html", "--cov-report=term"])
    
    if verbose:
        cmd.append("-v")
    
    return run_command(cmd)


def run_fast_tests(verbose=False):
    """Run fast tests only (exclude slow tests)."""
    cmd = ["uv", "run", "pytest", "-m", "not slow"]
    if verbose:
        cmd.append("-v")
    return run_command(cmd)


def run_parallel_tests(workers=4, verbose=False):
    """Run tests in parallel."""
    cmd = ["uv", "run", "pytest", "-n", str(workers)]
    if verbose:
        cmd.append("-v")
    return run_command(cmd)


def generate_html_report():
    """Generate HTML test report."""
    cmd = ["uv", "run", "pytest", "--html=reports/report.html", "--self-contained-html"]
    return run_command(cmd)


def run_lint():
    """Run linting tools."""
    print("Running flake8...")
    if not run_command(["uv", "run", "flake8", "src/", "tests/"]):
        return False
    
    print("Running black check...")
    if not run_command(["uv", "run", "black", "--check", "src/", "tests/"]):
        return False
    
    print("Running isort check...")
    if not run_command(["uv", "run", "isort", "--check-only", "src/", "tests/"]):
        return False
    
    return True


def format_code():
    """Format code with black and isort."""
    print("Formatting with black...")
    if not run_command(["uv", "run", "black", "src/", "tests/"]):
        return False
    
    print("Sorting imports with isort...")
    if not run_command(["uv", "run", "isort", "src/", "tests/"]):
        return False
    
    return True


def main():
    parser = argparse.ArgumentParser(description="Test runner for Flask Todo App")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--coverage", "-c", action="store_true", help="Run with coverage")
    parser.add_argument("--parallel", "-p", type=int, metavar="N", help="Run tests in parallel with N workers")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Test commands
    subparsers.add_parser("unit", help="Run unit tests")
    subparsers.add_parser("integration", help="Run integration tests")
    subparsers.add_parser("api", help="Run API tests")
    subparsers.add_parser("slow", help="Run slow/performance tests")
    subparsers.add_parser("fast", help="Run fast tests only")
    subparsers.add_parser("all", help="Run all tests")
    
    # Report commands
    subparsers.add_parser("report", help="Generate HTML test report")
    
    # Code quality commands
    subparsers.add_parser("lint", help="Run linting tools")
    subparsers.add_parser("format", help="Format code")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Ensure reports directory exists
    os.makedirs("reports", exist_ok=True)
    
    success = True
    
    if args.command == "unit":
        success = run_unit_tests(args.verbose)
    elif args.command == "integration":
        success = run_integration_tests(args.verbose)
    elif args.command == "api":
        success = run_api_tests(args.verbose)
    elif args.command == "slow":
        success = run_slow_tests(args.verbose)
    elif args.command == "fast":
        success = run_fast_tests(args.verbose)
    elif args.command == "all":
        if args.parallel:
            success = run_parallel_tests(args.parallel, args.verbose)
        else:
            success = run_all_tests(args.verbose, args.coverage)
    elif args.command == "report":
        success = generate_html_report()
    elif args.command == "lint":
        success = run_lint()
    elif args.command == "format":
        success = format_code()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()