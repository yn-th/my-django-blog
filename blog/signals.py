from django.db.models.signals import post_init, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse
from .models import Post, Notification , Profile

@receiver(post_save , sender=User)
def create_profile(sender , instance , created , **kwargs):
    if created:
        Profile.objects.create(user = instance)


# ۱. ذخیره وضعیت قبلی هنگام بارگذاری نمونه
@receiver(post_init, sender=Post)
def store_previous_status(sender, instance, **kwargs):
    instance._old_status = instance.status

# ۲. بررسی تغییرات پس از ذخیره و ایجاد اعلان
@receiver(post_save, sender=Post)
def create_post_notification(sender, instance, created, **kwargs):
    if created:
        # پست کاملاً جدید
        if instance.status == Post.Status.REVIEW:
            # به ویرایشگران اعلان بفرست
            editors = User.objects.filter(Q(groups__name='Editors') | Q(is_superuser=True)).distinct()
            for editor in editors:
                Notification.objects.create(
                    user=editor,
                    message=f'پست جدیدی برای بررسی: "{instance.title}"',
                    link=reverse('blog:review_queue')
                )
    else:
        # پست به‌روزرسانی شده – مقایسه وضعیت قدیم و جدید
        old_status = getattr(instance, '_old_status', None)
        new_status = instance.status

        if old_status != new_status:
            if new_status == Post.Status.REVIEW:
                # دوباره برای بررسی فرستاده شده (مثلاً نویسنده ویرایش کرد)
                editors = User.objects.filter(Q(groups__name='Editors') | Q(is_superuser=True)).distinct()
                for editor in editors:
                    Notification.objects.create(
                        user=editor,
                        message=f'پست "{instance.title}" برای بررسی دوباره ارسال شد.',
                        link=reverse('blog:review_queue')
                    )

            elif old_status == Post.Status.REVIEW and new_status == Post.Status.PUBLISH:
                # تأیید و انتشار
                Notification.objects.create(
                    user=instance.author,
                    message=f'پست شما "{instance.title}" تأیید و منتشر شد.',
                    link=reverse('blog:detail', args=[instance.pk])
                )

            elif old_status == Post.Status.REVIEW and new_status == Post.Status.DRAFT:
                # برگشت به پیش‌نویس
                Notification.objects.create(
                    user=instance.author,
                    message=f'پست شما "{instance.title}" نیاز به ویرایش دارد و به پیش‌نویس برگشت داده شد.',
                    link=reverse('blog:detail', args=[instance.pk])
                )