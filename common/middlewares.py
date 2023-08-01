

def count_user_clicks_middleware(get_response):
    def middleware(request):
        clicks_count=request.session.get('clicks_count',0)
        request.session['clicks_count']=clicks_count+1
        request.clicks_count=clicks_count
        return get_response(request)

    return middleware