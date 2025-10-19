#!/usr/bin/env python3
"""
Script para executar diferentes tipos de testes da aplicação Flask.

Uso:
    python run_tests.py --all          # Executa todos os testes
    python run_tests.py --unit         # Executa apenas testes unitários
    python run_tests.py --integration  # Executa apenas testes de integração
    python run_tests.py --coverage     # Executa com relatório de cobertura
    python run_tests.py --verbose      # Executa com saída detalhada
"""

import argparse
import subprocess
import sys
import os


def run_command(cmd, description):
    """Executa um comando e mostra o resultado."""
    print(f"\n{'='*50}")
    print(f"🧪 {description}")
    print(f"{'='*50}")
    print(f"Executando: {' '.join(cmd)}")
    print()
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print(f"\n✅ {description} - SUCESSO!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} - FALHOU!")
        print(f"Código de saída: {e.returncode}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Executar testes da aplicação Flask")
    parser.add_argument("--all", action="store_true", help="Executar todos os testes")
    parser.add_argument("--unit", action="store_true", help="Executar apenas testes unitários")
    parser.add_argument("--integration", action="store_true", help="Executar apenas testes de integração")
    parser.add_argument("--coverage", action="store_true", help="Executar com relatório de cobertura")
    parser.add_argument("--verbose", action="store_true", help="Saída detalhada")
    parser.add_argument("--slow", action="store_true", help="Incluir testes lentos")
    
    args = parser.parse_args()
    
    # Se nenhuma opção foi especificada, executar todos os testes
    if not any([args.all, args.unit, args.integration, args.coverage]):
        args.all = True
    
    # Comandos base
    pytest_cmd = ["python", "-m", "pytest"]
    
    if args.verbose:
        pytest_cmd.extend(["-v", "-s"])
    
    success = True
    
    if args.coverage:
        # Testes com cobertura
        cmd = pytest_cmd + [
            "--cov=app", 
            "--cov-report=html", 
            "--cov-report=term-missing",
            "app_test.py"
        ]
        success &= run_command(cmd, "Executando testes com cobertura")
        
        print(f"\n📊 Relatório de cobertura HTML gerado em: htmlcov/index.html")
    
    elif args.unit:
        # Apenas testes unitários
        cmd = pytest_cmd + ["-m", "unit", "app_test.py"]
        success &= run_command(cmd, "Executando testes unitários")
    
    elif args.integration:
        # Apenas testes de integração
        cmd = pytest_cmd + ["-m", "integration", "app_test.py"]
        success &= run_command(cmd, "Executando testes de integração")
    
    elif args.all:
        # Todos os testes (exceto os lentos, a menos que especificado)
        cmd = pytest_cmd + ["app_test.py"]
        if not args.slow:
            cmd.extend(["-m", "not slow"])
        success &= run_command(cmd, "Executando todos os testes")
    
    # Resumo final
    print(f"\n{'='*60}")
    if success:
        print("🎉 TODOS OS TESTES PASSARAM!")
    else:
        print("💥 ALGUNS TESTES FALHARAM!")
    print(f"{'='*60}")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())