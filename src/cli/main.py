import click

@click.command()
@click.option('-f' , '--file', help='File to analyse', type=str)
def filename(file):
    extension = file.split('.')[-1]
    if (extension in ['txt', 'pcap', 'evtx', 'json', 'xml']):
        print('Supported extension')
    else:
        print('Unsupported extension')

if __name__ == '__main__':
    filename()