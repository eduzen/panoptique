from django.core.management.base import BaseCommand

from streaming.models import VideoCamera


class Command(BaseCommand):
    def handle(self, *args, **options):
        v = VideoCamera()
        v.analize(show_img=True)

        self.stdout.write(
            self.style.SUCCESS('Successfully closed poll "exit"')
        )
