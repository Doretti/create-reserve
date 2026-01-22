import click
from pathlib import Path
from datetime import datetime
import tarfile
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    handlers=[
        logging.FileHandler("backup.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

@click.command()
@click.option(
    '--source', '-s',
    required=True,
    help='Путь к папке, которую нужно архивировать (обязательно)'
)
@click.option(
    '--dest', '-d',
    required=True,
    help='Путь, куда сохранить архив (обязательно)'
)
def main(source, dest):
    sourceDir = Path(source).resolve()
    destDir = Path(dest).resolve()

    if not (sourceDir.exists() and sourceDir.is_dir()):
        logging.error(f"Неверно передан параметр --source/-s, он должен ссылаться на существующую директорию {sourceDir}")
        return
    
    destDir.mkdir(parents=True, exist_ok=True)
    
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

    fileName = sourceDir.name + '_backup_' + timestamp + '.tar.gz'
    archivePath = destDir / fileName

    start = datetime.now()
    logging.info(f"Архивация: {sourceDir} → {archivePath}")

    with tarfile.open(archivePath, "w:gz") as tar:
        tar.add(sourceDir, arcname=sourceDir.name)

    duration = (datetime.now() - start).total_seconds()

    logging.info(f"Готово! Архив создан за {duration:.2f} сек.")

if __name__ == '__main__':
    main()