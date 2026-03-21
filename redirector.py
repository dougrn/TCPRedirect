import asyncio
import json
import logging
import sys

# Configuração de Logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("TCPRedirector")

async def forward_data(reader, writer):
    """Encaminha dados de um stream para outro."""
    try:
        while True:
            data = await reader.read(4096)
            if not data:
                break
            writer.write(data)
            await writer.drain()
    except Exception as e:
        logger.debug(f"Erro no encaminhamento de dados: {e}")
    finally:
        writer.close()
        try:
            await writer.wait_closed()
        except:
            pass

async def handle_client(local_reader, local_writer, target_host, target_port):
    """Lida com uma nova conexão cliente e a redireciona para o destino."""
    client_addr = local_writer.get_extra_info('peername')
    logger.info(f"Nova conexão de {client_addr} -> Redirecionando para {target_host}:{target_port}")

    try:
        remote_reader, remote_writer = await asyncio.open_connection(target_host, target_port)
        
        # Cria duas tarefas para encaminhamento bidirecional
        await asyncio.gather(
            forward_data(local_reader, remote_writer),
            forward_data(remote_reader, local_writer)
        )
    except Exception as e:
        logger.error(f"Falha ao conectar ao destino {target_host}:{target_port}: {e}")
    finally:
        local_writer.close()
        try:
            await local_writer.wait_closed()
        except:
            pass
        logger.info(f"Conexão de {client_addr} encerrada.")

async def start_redirector(listen_port, target_host, target_port):
    """Inicia um servidor que escuta em uma porta e redireciona para outra."""
    server = await asyncio.start_server(
        lambda r, w: handle_client(r, w, target_host, target_port),
        '0.0.0.0', listen_port
    )

    addr = server.sockets[0].getsockname()
    logger.info(f"Servidor ouvindo em {addr} e redirecionando para {target_host}:{target_port}")

    async with server:
        await server.serve_forever()

async def main():
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        logger.error("Arquivo config.json não encontrado.")
        return
    except json.JSONDecodeError:
        logger.error("Erro ao ler config.json. Formato inválido.")
        return

    mappings = config.get("mappings", [])
    if not mappings:
        logger.warning("Nenhum mapeamento encontrado em config.json.")
        return

    tasks = []
    for mapping in mappings:
        listen_port = mapping.get("listen_port")
        target_host = mapping.get("target_host", "127.0.0.1")
        target_port = mapping.get("target_port")

        if listen_port and target_port:
            tasks.append(start_redirector(listen_port, target_host, target_port))
        else:
            logger.warning(f"Mapeamento inválido ignorado: {mapping}")

    if tasks:
        logger.info(f"Iniciando {len(tasks)} redirecionador(es)...")
        await asyncio.gather(*tasks)
    else:
        logger.error("Nenhum redirecionamento válido configurado.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Encerrando redirecionador...")
    except Exception as e:
        logger.critical(f"Erro fatal: {e}")
