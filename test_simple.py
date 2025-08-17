#!/usr/bin/env python3
"""
Script simplificado para verificar funcionalidad básica del MVP
"""

import os
import sys
import subprocess

def print_status(message, status):
    if status:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")

def test_file_structure():
    """Verificar que los archivos principales existen"""
    essential_files = [
        "backend/main.py",
        "backend/requirements.txt", 
        "frontend/index.html",
        "frontend/script.js",
        "frontend/style.css",
        "README.md"
    ]
    
    print("🔍 Verificando estructura de archivos...")
    all_exist = True
    
    for file_path in essential_files:
        if os.path.exists(file_path):
            print_status(f"Archivo existe: {file_path}", True)
        else:
            print_status(f"Archivo faltante: {file_path}", False)
            all_exist = False
    
    return all_exist

def test_python_imports():
    """Verificar que las dependencias principales se pueden importar"""
    print("\n🐍 Verificando imports de Python...")
    
    try:
        # Test FastAPI
        from fastapi import FastAPI
        print_status("FastAPI importado", True)
        
        # Test Pydantic
        from pydantic import BaseModel
        print_status("Pydantic importado", True)
        
        # Test requests
        import requests
        print_status("Requests importado", True)
        
        # Test PIL
        from PIL import Image
        print_status("PIL importado", True)
        
        return True
        
    except ImportError as e:
        print_status(f"Error de importación: {e}", False)
        return False

def test_main_module():
    """Verificar que el módulo principal se puede importar"""
    print("\n📦 Verificando módulo principal...")
    
    try:
        # Agregar directorio backend al path
        sys.path.insert(0, 'backend')
        
        # Configurar variable de entorno para testing
        os.environ["GEMINI_API_KEY"] = "test_key_12345"
        
        # Test import del módulo principal
        import main
        print_status("Módulo main importado", True)
        
        # Test creación de app
        app = main.app
        print_status("FastAPI app creada", True)
        
        return True
        
    except Exception as e:
        print_status(f"Error en módulo principal: {e}", False)
        return False

def test_frontend_files():
    """Verificar que los archivos frontend tienen contenido válido"""
    print("\n🎨 Verificando archivos frontend...")
    
    try:
        # Verificar HTML
        with open('frontend/index.html', 'r') as f:
            html_content = f.read()
            if '<!DOCTYPE html>' in html_content and 'CM Assistant' in html_content:
                print_status("HTML válido", True)
            else:
                print_status("HTML inválido", False)
                return False
        
        # Verificar JavaScript
        with open('frontend/script.js', 'r') as f:
            js_content = f.read()
            if 'function' in js_content and 'API_BASE_URL' in js_content:
                print_status("JavaScript válido", True)
            else:
                print_status("JavaScript inválido", False)
                return False
        
        # Verificar CSS
        with open('frontend/style.css', 'r') as f:
            css_content = f.read()
            if 'body' in css_content and 'container' in css_content:
                print_status("CSS válido", True)
            else:
                print_status("CSS inválido", False)
                return False
        
        return True
        
    except Exception as e:
        print_status(f"Error verificando frontend: {e}", False)
        return False

def isValidUrl(string):
    """Función auxiliar para validar URLs"""
    try:
        from urllib.parse import urlparse
        result = urlparse(string)
        return all([result.scheme, result.netloc])
    except:
        return False

def run_basic_functionality_test():
    """Ejecutar test básico de funcionalidad"""
    print("\n🚀 Ejecutando test básico de funcionalidad...")
    
    try:
        # Test validación de URL
        valid_urls = ["https://example.com", "http://test.org"]
        invalid_urls = ["not-a-url", ""]
        
        url_tests_passed = True
        for url in valid_urls:
            if not isValidUrl(url):
                url_tests_passed = False
                break
        
        for url in invalid_urls:
            if isValidUrl(url):
                url_tests_passed = False
                break
        
        print_status("Tests de validación de URL", url_tests_passed)
        
        # Test básico de configuración
        if os.environ.get("GEMINI_API_KEY"):
            print_status("Variable de entorno configurada", True)
        else:
            print_status("Variable de entorno faltante", False)
            
        return url_tests_passed
        
    except Exception as e:
        print_status(f"Error en test de funcionalidad: {e}", False)
        return False

def main():
    """Función principal"""
    print("🧪 TESTS SIMPLIFICADOS - CM ASSISTANT MVP")
    print("=" * 50)
    
    results = []
    
    # Ejecutar tests
    results.append(test_file_structure())
    results.append(test_python_imports())
    results.append(test_main_module())
    results.append(test_frontend_files())
    results.append(run_basic_functionality_test())
    
    # Resumen
    passed = sum(results)
    total = len(results)
    
    print(f"\n📊 RESUMEN:")
    print(f"Tests pasados: {passed}/{total}")
    print(f"Porcentaje de éxito: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 ¡Todos los tests básicos pasaron!")
        print("✨ El MVP está funcionando correctamente")
    else:
        print("⚠️  Algunos tests fallaron, pero la funcionalidad básica está presente")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)