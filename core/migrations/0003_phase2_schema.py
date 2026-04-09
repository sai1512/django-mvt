from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


def create_default_course(apps, schema_editor):
    Course = apps.get_model('core', 'Course')
    database_alias = schema_editor.connection.alias

    if not Course.objects.using(database_alias).filter(pk=1).exists():
        Course.objects.using(database_alias).create(
            id=1,
            name='Unassigned',
            code='UNASSIGNED',
            description='Placeholder course for existing student records.',
        )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_student_course_id'),
    ]

    operations = [
        migrations.RunPython(create_default_course, migrations.RunPython.noop),
        migrations.AddField(
            model_name='student',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='grade',
            field=models.CharField(default='N/A', max_length=2),
        ),
        migrations.AddField(
            model_name='student',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='student',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='core.course'),
            preserve_default=False,
        ),
    ]