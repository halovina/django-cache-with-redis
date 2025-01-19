import json
from django.conf import settings
from datetime import timedelta

cache = settings.REDIS_INSTANCE

def simpan_data_redis(key, data, expired_time=900):
    """
    Menyimpan data ke Redis dengan waktu kadaluarsa.

    Args:
        key: key untuk menyimpan data di Redis (string).
        data: Data yang akan disimpan (bisa berupa string, list, atau dictionary).
        expired_time: Waktu kadaluarsa data (timedelta). Default 5 menit.
    """
    try:
        # Konversi data ke string JSON jika bukan string
        if not isinstance(data, str):
            data = json.dumps(data)
        cache.set(key, data, ex=expired_time)
        return True
    except Exception as e:
        print(f"Error menyimpan data ke Redis: {e}")
        return False

def ambil_data_redis(key):
    """
    Mengambil data dari Redis berdasarkan key.

    Args:
        key: key data di Redis (string).

    Returns:
        Data yang diambil dari Redis, atau None jika key tidak ditemukan.
    """
    try:
        data = cache.get(key)
        if data:
            try:
                # Coba parse data sebagai JSON, jika berhasil berarti data asalnya bukan string
                return json.loads(data)
            except json.JSONDecodeError:
                return data # Jika gagal parse JSON, kembalikan data apa adanya (bertipe string)
        return None
    except Exception as e:
        print(f"Error mengambil data dari Redis: {e}")
        return None

def hapus_data_redis(key):
    """
    Menghapus data dari Redis berdasarkan key.

    Args:
        key: key data di Redis (string).
    """
    try:
        cache.delete(key)
        return True
    except Exception as e:
        print(f"Error menghapus data dari Redis: {e}")
        return False

