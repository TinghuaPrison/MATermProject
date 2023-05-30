package com.tsinghua.ss.client;

import okhttp3.MultipartBody;
import okhttp3.RequestBody;
import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.http.Field;
import retrofit2.http.FormUrlEncoded;
import retrofit2.http.POST;
import retrofit2.http.Part;

public interface ApiService {
    // 用户注册
    @FormUrlEncoded
    @POST("user_register/")
    Call<ResponseBody> userRegister(
            @Field("username") String username,
            @Field("password") String password,
            @Part("avatar") MultipartBody.Part avatar,
            @Field("bio") String bio
    );

    // 用户登录
    @FormUrlEncoded
    @POST("user_login/")
    Call<ResponseBody> userLogin(
            @Field("username") String username,
            @Field("password") String password
    );

    // 用户编辑
    @FormUrlEncoded
    @POST("user_edit/")
    Call<ResponseBody> userEdit(
            @Field("username") String username,
            @Field("newname") String newname,
            @Field("password") String password,
            @Part("avatar") RequestBody avatar,
            @Field("bio") String bio
    );

    // 获取所有用户
    @POST("get_all_users/")
    Call<ResponseBody> getAllUsers();

    // 获取单个用户
    @FormUrlEncoded
    @POST("get_user/")
    Call<ResponseBody> getUser(
            @Field("username") String username
    );
}
