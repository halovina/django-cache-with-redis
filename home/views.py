from django.shortcuts import render
from django.http import JsonResponse
from .redisclient import simpan_data_redis, ambil_data_redis, hapus_data_redis
from datetime import timedelta
# from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def redis_manage_data(request):
    key = "data_pengguna"
    if request.method == 'POST':
        nama = request.POST.get('nama')
        umur = request.POST.get('umur')
        data_baru = {"nama": nama, "umur": umur}
        if simpan_data_redis(key, data_baru, expired_time=100): # Expired 10 detik
            return JsonResponse({"status": "berhasil", "pesan": "Data berhasil disimpan di Redis"})
        else:
            return JsonResponse({"status": "gagal", "pesan": "Gagal menyimpan data di Redis"}, status=500)

    elif request.method == 'GET':
        data_di_redis = ambil_data_redis(key)
        if data_di_redis:
            return JsonResponse({"status": "berhasil", "data": data_di_redis})
        else:
            return JsonResponse({"status": "gagal", "pesan": "Data tidak ditemukan di Redis"}, status=404)


    elif request.method == 'DELETE':
        if hapus_data_redis(key):
            return JsonResponse({"status": "berhasil", "pesan": "Data berhasil dihapus dari Redis"})
        else:
            return JsonResponse({"status": "gagal", "pesan": "Gagal menghapus data dari Redis"}, status=500)

    return JsonResponse({"status":"error", "pesan": "Method tidak diizinkan"}, status=405)

