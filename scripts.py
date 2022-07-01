import random

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from datacenter.models import Mark, Schoolkid, Chastisement, Lesson, Subject, Commendation


def fix_marks(name):
    try:
        schoolkid = fetch_schoolkid(name)
        Mark.objects.filter(schoolkid=schoolkid, points__lt=4).update(points=5)
    except ObjectDoesNotExist:
        print(f'Не найдено ни одного урока ученика "{name}"')
    except MultipleObjectsReturned:
        print('Найдено более одной записи, уточните ФИО ученика')


def del_chastisements(name):
    try:
        schoolkid = fetch_schoolkid(name)
        Chastisement.objects.filter(schoolkid=schoolkid).delete()
    except ObjectDoesNotExist:
        print(f'Не найдено ни одного урока ученика "{name}"')
    except MultipleObjectsReturned:
        print('Найдено более одной записи, уточните ФИО ученика')


def create_commendation(name, subject_name):
    commendation_texts = [
        'Молодец!',
        'Отлично!',
        'Хорошо!',
        'Гораздо лучше, чем я ожидал!',
        'Ты меня приятно удивил!',
        'Великолепно!',
        'Прекрасно!',
        'Ты меня очень обрадовал!',
        'Именно этого я давно ждал от тебя!',
        'Сказано здорово – просто и ясно!',
        'Ты, как всегда, точен!',
        'Очень хороший ответ!',
        'Талантливо!',
        'Ты сегодня прыгнул выше головы!',
        'Я поражен!',
        'Уже существенно лучше!',
        'Потрясающе!',
        'Замечательно!',
        'Прекрасное начало!',
        'Так держать!',
        'Ты на верном пути!',
        'Здорово!',
        'Это как раз то, что нужно!',
        'Я тобой горжусь!',
        'С каждым разом у тебя получается всё лучше!',
        'Мы с тобой не зря поработали!',
        'Я вижу, как ты стараешься!',
        'Ты растешь над собой!',
        'Ты многое сделал, я это вижу!',
        'Теперь у тебя точно все получится!',
    ]
    try:
        schoolkid = fetch_schoolkid(name)
        subject = Subject.objects.get(title__contains=subject_name, year_of_study=schoolkid.year_of_study)

        commendation_text = random.choice(commendation_texts)
        commendations = Commendation.objects.filter(schoolkid=schoolkid, subject=subject)
        commendations_dates = []
        for commendation in commendations:
            commendations_dates.append(commendation.created)
        lessons = Lesson.objects.filter(
            year_of_study=schoolkid.year_of_study,
            group_letter=schoolkid.group_letter,
            subject=subject,
        ).exclude(date__in=commendations_dates)
        lesson = random.choice(lessons)
        Commendation.objects.create(
            text=commendation_text,
            created=lesson.date,
            schoolkid=schoolkid,
            subject=lesson.subject,
            teacher=lesson.teacher
        )

    except ObjectDoesNotExist:
        print(f'Не найдено ни одного урока "{subject_name}" или ученика "{name}"')
    except MultipleObjectsReturned:
        print('Найдено более одной записи, уточните ФИО ученика')


def fetch_schoolkid(name):
    schoolkid = Schoolkid.objects.get(full_name__contains=name)
    return schoolkid
