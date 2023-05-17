package com.tsinghua.ss.client.api;

import com.tsinghua.ss.client.bean.Post;
import com.tsinghua.ss.client.bean.User;

import java.util.List;
import java.util.Map;

import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.FieldMap;
import retrofit2.http.FormUrlEncoded;
import retrofit2.http.GET;
import retrofit2.http.POST;

public interface Api {
    @GET("post/")
    Call<List<Post>> getAllPosts();

    @FormUrlEncoded
    @POST("login/")
    Call<ResponseBody> login(@FieldMap Map<String, String> params);

    @FormUrlEncoded
    @POST("register/")
    Call<ResponseBody> register(@FieldMap Map<String, String> params);
}
