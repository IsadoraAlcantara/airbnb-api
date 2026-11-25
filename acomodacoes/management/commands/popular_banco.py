import io
import random
from decimal import Decimal
from faker import Faker
from PIL import Image as PilImage

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction

from acomodacoes.models import Acomodacao, ImagemAcomodacao

Usuario = get_user_model()
fake = Faker("pt_BR")


def gerar_imagem_ficticia(nome_arquivo):
    cor_rgb = (
        random.randint(40, 220),
        random.randint(40, 220),
        random.randint(40, 220),
    )
    img = PilImage.new("RGB", (800, 600), color=cor_rgb)
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=80)
    return ContentFile(buffer.getvalue(), name=nome_arquivo)


class Command(BaseCommand):
    help = "Gera acomodações e imagens em massa usando Faker."

    def add_arguments(self, parser):
        parser.add_argument(
            "--quantidade",
            type=int,
            default=20,
            help="Número de acomodações a serem criadas (padrão: 20)",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        quantidade = options["quantidade"]
        self.stdout.write(f"Gerando {quantidade} acomodações...")

        # Cria 3 anfitriões diferentes para variar os donos
        anfitrioes = []
        for i in range(1, 4):
            user, criado = Usuario.objects.get_or_create(
                username=f"anfitriao_{i}",
                defaults={
                    "email": fake.unique.email(),
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name(),
                    "cpf": fake.unique.cpf().replace(".", "").replace("-", ""),
                    "telefone": f"479{random.randint(80000000, 99999999)}",
                },
            )
            if criado:
                user.set_password("senha123")
                user.save()
            anfitrioes.append(user)

        tipos = ["Casa", "Apartamento", "Barco", "Cabana", "Gruta", "Hotel", "Pousada", "Trailer"]
        adjetivos = ["Aconchegante", "Moderno", "com Vista", "Pé na Areia", "no Centro", "Espaçoso", "Rústico"]
        categorias = [c[0] for c in Acomodacao.CategoriaAcomodacao.choices]

        for _ in range(quantidade):
            tipo = random.choice(tipos)
            cidade = fake.city()
            quartos = random.randint(1, 5)

            acomodacao = Acomodacao.objects.create(
                titulo_acomodacao=f"{tipo} {random.choice(adjetivos)} em {cidade}"[:50],
                valor_diaria=Decimal(random.randrange(90, 1200)) + Decimal("0.00"),
                qtd_quartos=quartos,
                qtd_banheiros=random.randint(1, quartos + 1),
                qtd_camas=random.randint(quartos, quartos * 2),
                max_hospedes=random.randint(2, quartos * 3),
                categoria_acomodacao=random.choice(categorias),
                tipo_acomodacao=tipo,
                descricao_acomodacao=fake.text(max_nb_chars=480),
                status_hospedagem=random.choices(
                    [Acomodacao.Status.PUBLISHED, Acomodacao.Status.DRAFT],
                    weights=[85, 15],  # 85% publicadas, 15% rascunho
                )[0],
                logradouro=fake.street_name()[:150],
                numero_hospedagem=str(random.randint(10, 2500)),
                bairro=fake.bairro()[:100],
                cidade=cidade[:100],
                estado=fake.estado_sigla(),
                cep=fake.postcode()[:9],
                proprietario=random.choice(anfitrioes),
            )

            # Cria entre 2 e 4 imagens por acomodação
            for idx in range(1, random.randint(3, 5)):
                ImagemAcomodacao.objects.create(
                    acomodacao=acomodacao,
                    imagem=gerar_imagem_ficticia(f"acom_{acomodacao.id}_{idx}.jpg"),
                    ordem=idx,
                )

        self.stdout.write(self.style.SUCCESS(f"{quantidade} acomodações criadas com sucesso!"))