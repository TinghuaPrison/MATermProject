package com.tsinghua.ss.client;

import com.tsinghua.ss.client.ApiService;

import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.RequestBody;
import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

import java.io.File;

public class ApiClient {
    private static final String BASE_URL = "http://your-server-host/";

    private ApiService apiService;

    public ApiClient() {
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl(BASE_URL)
                .addConverterFactory(GsonConverterFactory.create())
                .client(new OkHttpClient.Builder().build())
                .build();

        apiService = retrofit.create(ApiService.class);
    }

    public void userRegister(String username, String password, File avatar, String bio) {
        MultipartBody.Part avatarPart = null;
        if (avatar != null) {
            RequestBody avatarFile = RequestBody.create(MediaType.parse("image/*"), avatar);
            avatarPart = MultipartBody.Part.createFormData("avatar", avatar.getName(), avatarFile);
        }

        Call<ResponseBody> call = apiService.userRegister(username, password, avatarPart, bio);
        call.enqueue(new Callback<ResponseBody>() {
            @Override
            public void onResponse(Call<ResponseBody> call, Response<ResponseBody> response) {
                // 处理响应
                if (response.isSuccessful()) {
                    // 注册成功
                } else {
                    // 注册失败
                }
            }

            @Override
            public void onFailure(Call<ResponseBody> call, Throwable t) {
                // 处理请求失败
            }
        });
    }

    // 其他接口方法的类似实现...
}
