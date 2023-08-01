from main_app.models import PetPhoto


def count_user_clicks_middleware(get_response):
    def middleware(request):
        clicks_count=request.session.get('clicks_count',0)
        request.session['clicks_count']=clicks_count+1
        request.clicks_count=clicks_count
        return get_response(request)

    return middleware


def last_viewed_pet_photos_middleware(get_response):
    def middleware(request):
        viewed_pet_photos=request.session.get('last_viewed_pet_photos_ids',[])
        pets = PetPhoto.objects.filter(id__in=viewed_pet_photos)
        request.last_viewed_pet_photos=pets
        return get_response(request)

    return middleware