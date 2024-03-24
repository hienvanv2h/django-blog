from django.db import models
from django.contrib.auth.models import User
from PIL import Image

default_img = "default.jpg"
upload_dir = "profile_pics"

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  image = models.ImageField(default=default_img, upload_to=upload_dir)
  # Define you fields here...

  def __str__(self) -> str:
    return f"{self.user.username} Profile"

  # def save(self, *args, **kwargs):
  #   p = Profile.objects.get(id=self.pk)
  #   if p.image == default_img:
  #     pass
  #   elif p.image != self.image:
  #     p.image.delete(save=False)

  #   super().save(*args, **kwargs)
  #   img = Image.open(self.image.path)
  #   if img.height > 300 or img.width > 300:
  #     output_size = (300, 300)
  #     img.thumbnail(output_size)
  #     img.save(self.image.path)   # override original image