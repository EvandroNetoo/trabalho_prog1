import os
from dataclasses import dataclass
from typing import Any, Callable, TypeVar, Union

T = TypeVar('T')


@dataclass
class Funcionario:
    matricula: int
    salario: float

    def aumentar_salario(self, aumento: float) -> float:
        self.salario *= 1 + aumento / 100
        return self.salario


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def limpar_terminal() -> None:
    os.system('cls||clear')


def print_error(value: Any) -> None:
    print(Colors.FAIL + value + Colors.ENDC)


def print_cabecalho(value: Any) -> None:
    limpar_terminal()
    print(Colors.OKBLUE + value + '\n' + Colors.ENDC)


def print_sucesso(value: Any) -> None:
    print('\n' + Colors.OKGREEN + value + Colors.ENDC)


def input_tipo_valido(prompt: str = '', tipo: Callable[[str], T] = str) -> T:
    try:
        input_usuario = tipo(input(prompt + Colors.OKCYAN))
        print(end=Colors.ENDC)
        return input_usuario
    except ValueError:
        print_error(f'O valor digitado deve ser do tipo {tipo.__name__}.')
        return input_tipo_valido(prompt, tipo)


def menu() -> str:
    texto_menu = """FOLHA DE PAGAMENTO

1 - Inserir funcionário
2 - Pesquisar por matricula
3 - Aumentar salario
4 - Maior salário
5 - Demitir
6 - Listar
0 - Sair
Escolha sua opção: """
    escolha = input(texto_menu + Colors.OKCYAN)
    print(end=Colors.ENDC)
    return escolha.strip()


def gerar_funcionario() -> Funcionario:
    matricula = input_tipo_valido('Número da matrícula: ', int)
    salario = input_tipo_valido('Salário: ', float)
    while salario <= 0:
        print_error('Salário deve ser maior que 0.')
        salario = input_tipo_valido('Salário: ', float)
    return Funcionario(matricula, salario)


def listar_funcionarios(funcionarios: list[Funcionario]) -> None:
    def print_separador():
        print(
            '+'
            + '-' * (maior_tamanho_matricula + 2)
            + '+'
            + '-' * (maior_tamanho_salario + 2)
            + '+'
        )

    matricula = 'Matrícula'
    salario = 'Salário'
    maior_tamanho_matricula = len(
        max(
            matricula,
            *[str(funcionario.matricula) for funcionario in funcionarios],
            key=len,
        )
    )
    maior_tamanho_salario = len(
        max(
            salario,
            *[str(funcionario.salario) for funcionario in funcionarios],
            key=len,
        )
    )

    print_separador()
    print(
        f'| {matricula:<{maior_tamanho_matricula}} '
        + f'| {salario:<{maior_tamanho_salario}} |'
    )
    print_separador()

    for funcionario in funcionarios:
        print(
            f'| {funcionario.matricula:<{maior_tamanho_matricula}} '
            + f'| {funcionario.salario:<{maior_tamanho_salario}} |'
        )
        print_separador()


def get_funcionario(
    funcionarios: list[Funcionario], matricula: int
) -> Union[Funcionario, None]:
    funcionario = list(
        filter(
            lambda funcionario: funcionario.matricula == matricula,
            funcionarios,
        )
    )
    return None if not funcionario else funcionario[0]


def main():
    limpar_terminal()
    funcionarios: list[Funcionario] = [Funcionario(1, 1)]

    escolha = ''
    while escolha != '0':
        escolha = menu()

        match escolha:
            case '0':
                break

            case '1':
                print_cabecalho('Inserir funcionário')

                funcionario = gerar_funcionario()
                if get_funcionario(funcionarios, funcionario.matricula):
                    print_error(
                        'Não foi possível realizar o cadastro.'
                        + f'\nFuncionário com a matrícula {funcionario.matricula} já está cadastrado.'
                    )
                else:
                    funcionarios.append(funcionario)
                    print_sucesso('Funcionário adicionado com sucesso.')

            case '2':
                print_cabecalho('Pesquisar por matrícula')

                matricula = input_tipo_valido('Matrícula: ', int)
                funcionario = get_funcionario(funcionarios, matricula)
                if not funcionario:
                    print_error(f'Mátricula {matricula} não encontrada.')
                else:
                    listar_funcionarios(funcionario)

            case '3':
                print_cabecalho('Demitir funcionário')

                matricula = input_tipo_valido('Matrícula: ', int)
                aumento = input_tipo_valido('Aumento: ', float)

                funcionario = get_funcionario(funcionarios, matricula)
                if not funcionario:
                    print_error(f'Mátricula {matricula} não encontrada.')

                funcionario.aumentar_salario(aumento)
                print_sucesso(
                    f'Funcionário com matrícula {matricula} teve o aumento de {aumento:.1f}%.'
                )

            case '4':
                print_cabecalho('Maior salário')

                if not funcionarios:
                    print_error('Nenhum funcionário cadastrado.')

                else:
                    funcionario_maior_salario = [
                        sorted(
                            funcionarios,
                            key=lambda funcionario: -funcionario.salario,
                        )[0]
                    ]
                    listar_funcionarios(funcionario_maior_salario)

            case '5':
                print_cabecalho('Demitir funcionário')

                matricula = input_tipo_valido('Matrícula: ', int)

                funcionario = get_funcionario(funcionarios, matricula)
                if not funcionario:
                    print_error(f'Mátricula {matricula} não encontrada.')
                else:
                    funcionarios.remove(funcionario[0])
                    print_sucesso(
                        f'Funcionário com matrícula {matricula} demitido com sucesso.'
                    )

            case '6':
                print_cabecalho('Listar funcionários')

                if not funcionarios:
                    print_error('Nenhum funcionário cadastrado.')
                else:
                    listar_funcionarios(funcionarios)

            case _:
                print_error(f'\n{escolha} é uma opção inválida.')

        input('\nPressione <enter> para continuar...')
        limpar_terminal()

    limpar_terminal()
    print('Programa finalizado.')


if __name__ == '__main__':
    main()
