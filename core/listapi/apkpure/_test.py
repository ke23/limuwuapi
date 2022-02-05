# FILE INI HANYA UNTUK MENCOBA SCRIPT SCRAPERNYA APAKAH BERHASIL RETURN
# JIKA SUDAH SUCCESS MAKAN BISA DILANJUT KE API NYA


from pure_class import ApkPure

apk = ApkPure()

# print("i am hereeeee")
# print(kwargs)
# # get_query = request.GET.get('q', None)
s = apk.search_apk('music')
# response = Response(s)
print(s)
# return response
