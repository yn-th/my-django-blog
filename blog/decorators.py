from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def group_required(*group_names):
    """دکوراتوری که بررسی می‌کند کاربر در یکی از گروه‌های داده‌شده عضو باشد."""
    def in_groups(user):
        if user.is_superuser:
            return True
        return user.groups.filter(name__in=group_names).exists()
    return user_passes_test(in_groups, login_url='login')