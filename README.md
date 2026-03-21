# 🚀 TCPRedirect

**TCPRedirect** é um proxy TCP poderoso e leve escrito em Python utilizando `asyncio`. Ele permite redirecionar o tráfego de uma ou mais portas locais para qualquer outro host e porta especificados.

Esta ferramenta foi projetada especificamente para contornar restrições de acesso baseadas em IP (como bloqueios de `localhost`), fazendo o proxy de conexões externas através de uma instância local para que pareçam vir do próprio `localhost`.

---

## 🌟 Características

-   **Suporte Multi-Porta**: Redirecione múltiplas portas simultaneamente em uma única instância.
-   **Performance Async**: Construído sobre o `asyncio` do Python para alta concorrência e baixo consumo de recursos.
-   **Configuração Simples**: Gerenciamento fácil via `config.json` para todos os seus mapeamentos.
-   **Logs Profissionais**: Logs limpos com data/hora para monitorar o fluxo de dados em tempo real.
-   **Encerramento Seguro**: Lida corretamente com sinais de interrupção para garantir que todas as conexões sejam fechadas com segurança.

---

## 📂 Estrutura do Projeto

```text
TCPRedirect/
├── config.json         # Configuração dos mapeamentos de porta
├── redirector.py       # Lógica central do proxy
├── .gitignore          # Regras de arquivos ignorados pelo Git
└── README.md           # Documentação
```

---

## 🛠️ Instalação

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/dougrn/TCPRedirect.git
    cd TCPRedirect
    ```

2.  **Certifique-se de ter o Python 3.7+ instalado.**

3.  **Sem dependências externas!** (Utiliza a biblioteca padrão do Python).

---

## 🚀 Como Usar

### 1. Configurar Mapeamentos
Edite o arquivo `config.json` para definir seus redirecionamentos. Cada mapeamento consiste em:
-   `listen_port`: A porta que o TCPRedirect irá ouvir.
-   `target_host`: O host de destino (ex: `127.0.0.1`).
-   `target_port`: A porta de destino.

```json
{
  "mappings": [
    {
      "comment": "Redireciona a porta externa 8091 para a local 8090",
      "listen_port": 8091,
      "target_host": "127.0.0.1",
      "target_port": 8090
    }
  ]
}
```

### 2. Executar o Redirecionador
```bash
python redirector.py
```

---

## 💡 Como Funciona

Quando o TCPRedirect recebe uma conexão em uma `listen_port`, ele estabelece uma nova conexão com o `target_host:target_port`. Em seguida, cria uma ponte bidirecional, encaminhando todos os dados entre o cliente original e o serviço de destino.

Como o TCPRedirect geralmente roda na mesma máquina que o serviço de destino, este vê a conexão vindo de `127.0.0.1`, ignorando efetivamente as restrições de acesso baseadas em IP.

---

## 📜 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.

---

Desenvolvido com ❤️ por [dougrn](https://github.com/dougrn)
