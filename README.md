# ControlVision - Mini Sistema Supervisório de Monitoramento Fábril

Esse repositório contém o código de implementação de um sistema de monitoramente fábril utilizando-se câmeras e sensores genéricos. A aplicação consite em ser um mini sistema supervisório com o seu frontend implementando em QT (Python) e a principal lógica de backend implementada em FastAPI (Python). O sistema é integrado com Docker Swarm, que tem alguns componentes adicionais como o Grafana para visualização de dados.

As principais features do sistema são:
- Cadastro e Divisão do Sistema de Acordo com a Categoria do Funcionário
- Interface Gráfica de Sistema Supervisório em Dip-Down, com observações, alarmes e informações de produtividade de cada funcionário
