# @author Derek Christopher
# -*- coding: utf-8 -*-

import re

def auditar_senha_validador(senha):
    print(f"\n[*] Auditando política de segurança para a senha: '{senha}'")
    
    if len(senha) < 12:
        print("\033[91m[-] Reprovado: A senha deve ter no mínimo 12 caracteres.\033[0m")
        return False
    if not re.search("[A-Z]", senha):
        print("\033[91m[-] Reprovado: Faltam letras maiúsculas.\033[0m")
        return False
    if not re.search("[a-z]", senha):
        print("\033[91m[-] Reprovado: Faltam letras minúsculas.\033[0m")
        return False
    if not re.search("[0-9]", senha):
        print("\033[91m[-] Reprovado: Faltam números.\033[0m")
        return False
    if not re.search("[!@#$%^&*(),.?\":{}|<>]", senha):
        print("\033[91m[-] Reprovado: Faltam caracteres especiais.\033[0m")
        return False
        
    print("\033[92m[✓] Aprovado! Senha considerada forte para os nós validadores.\033[0m")
    return True

# Massa de testes operacionais
auditar_senha_validador("123456")
auditar_senha_validador("Fsociety2026")
auditar_senha_validador("Control#Op@Fsociety2026")
