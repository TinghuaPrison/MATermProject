package com.tsinghua.ss.client;

import android.app.Application;

import cn.leancloud.LeanCloud;

public class ClientApplication extends Application {
    @Override
    public void onCreate() {
        super.onCreate();
        LeanCloud.initialize(this, "pnaeKJxT0Hofs0ekFpLBAnFG-gzGzoHsz", "nmkw2bum5gDuuOEZIcP09TJH", "https://pnaekjxt.lc-cn-n1-shared.com");
    }
}
