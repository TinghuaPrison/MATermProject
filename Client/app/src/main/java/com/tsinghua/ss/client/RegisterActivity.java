package com.tsinghua.ss.client;

import androidx.activity.result.ActivityResult;
import androidx.activity.result.ActivityResultCallback;
import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContract;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;

import android.provider.MediaStore;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Toast;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintStream;
import java.sql.Time;
import java.util.ArrayList;

import cn.leancloud.LCFile;
import cn.leancloud.LCUser;
import de.hdodenhof.circleimageview.CircleImageView;
import io.reactivex.Observer;
import io.reactivex.disposables.Disposable;

public class RegisterActivity extends AppCompatActivity {

    private CircleImageView avatarImageView;
    private EditText usernameEditText;
    private EditText passwordEditText;
    private EditText bioEditText;
    private Button registerButton;
    private Uri selectedImageUri;
    private String uploadImageUri;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);
        avatarImageView = findViewById(R.id.avatar);
        usernameEditText = findViewById(R.id.username);
        passwordEditText = findViewById(R.id.password);
        bioEditText = findViewById(R.id.bio);
        registerButton = findViewById(R.id.register);

        avatarImageView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
                startActivityForResult(intent, 1);
            }
        });

        registerButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String username = usernameEditText.getText().toString();
                String password = passwordEditText.getText().toString();
                String bio = bioEditText.getText().toString();
                String fileName = String.valueOf(System.currentTimeMillis());
                try {
                    LCFile file = LCFile.withAbsoluteLocalPath(fileName, selectedImageUri.getPath());
                    file.saveInBackground().subscribe(new Observer<LCFile>() {
                        @Override
                        public void onSubscribe(Disposable d) {}
                        @Override
                        public void onNext(LCFile lcFile) {
                            uploadImageUri = lcFile.getUrl();
                        }
                        @Override
                        public void onError(Throwable e) {

                        }
                        @Override
                        public void onComplete() {}
                    });
                } catch (FileNotFoundException e) {
                    e.printStackTrace();
                }
                LCUser user = new LCUser();
                user.setUsername(username);
                user.setPassword(password);
                user.put("bio", bio);
                user.put("avatar", uploadImageUri);
                user.signUpInBackground().subscribe(new Observer<LCUser>() {
                    @Override
                    public void onSubscribe(Disposable d) {}
                    @Override
                    public void onNext(LCUser lcUser) {
                        CharSequence text = "注册成功";
                        Toast.makeText(getApplicationContext(), text, Toast.LENGTH_SHORT).show();
                        Intent intent = new Intent(getApplicationContext(), MainActivity.class);
                        startActivity(intent);
                    }

                    @Override
                    public void onError(Throwable e) {
                        CharSequence text = "注册失败";
                        Toast.makeText(getApplicationContext(), text, Toast.LENGTH_SHORT).show();
                    }
                    @Override
                    public void onComplete() {}
                });
            }
        });
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == 1 && resultCode == RESULT_OK && data != null && data.getData() != null) {
            selectedImageUri = data.getData();
            try {
                Bitmap bitmap = MediaStore.Images.Media.getBitmap(getContentResolver(), selectedImageUri);
                avatarImageView.setImageBitmap(bitmap);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}