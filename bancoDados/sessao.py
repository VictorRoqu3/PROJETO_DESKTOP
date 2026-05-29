class Sessao:
    """
    Classe Sessao — os caras do teto.

    Os caras do teto na maldade com a makita.

    Essa classe controla tudo isso com um único atributo de classe e alguns métodos.
    Você não precisa instanciar nada, só usar diretamente.

    Atributo:
    usuario_logado : object ou None
        É aqui que mora o usuário logado. Se for None, significa que ninguém está logado
        e os caras já estão na maldade.

    Métodos:
    login(usuario)
        Ativa a sessão com o usuário informado. A partir daqui, você tem acesso liberado.

    logout()
        Encerra a sessão atual. Adeus acesso. Os caras do teto na bondade.

    esta_logado()
        Retorna True se tiver alguém logado. Se não, retorna False e você 
        vai ser desconectado de tudo.

    """

    # Atributo que guarda o usuário logado 
    usuario_logado = None

    @classmethod
    def login(cls, usuario):
        """
        Registra um usuário como logado na sessão.

        usuario : object
            O objeto ou identificador do usuário que será marcado como logado.
        """
        cls.usuario_logado = usuario

    @classmethod
    def logout(cls):
        """
        Encerra a sessão atual, removendo o usuário logado.
        """
        cls.usuario_logado = None

    @classmethod
    def esta_logado(cls):
        """
        Verifica se há um usuário logado.

        bool
            True se um usuário estiver logado, False caso contrário.
        """
        return cls.usuario_logado is not None