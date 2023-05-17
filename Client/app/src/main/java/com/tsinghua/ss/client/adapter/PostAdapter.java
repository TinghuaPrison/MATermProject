package com.tsinghua.ss.client.adapter;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.recyclerview.widget.RecyclerView;

import com.tsinghua.ss.client.R;
import com.tsinghua.ss.client.bean.Post;

import java.util.List;

public class PostAdapter extends RecyclerView.Adapter<PostAdapter.ViewHolder> {
    private List<Post> posts;

    public PostAdapter(List<Post> posts) {
        this.posts = posts;
    }

    @Override
    public ViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.post_layout, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(ViewHolder holder, int position) {
        Post post = posts.get(position);
        holder.username.setText(post.getUsername());
        holder.post_time.setText(post.getC_time());
        holder.content.setText(post.getContent());
        holder.location.setText(post.getLocation());
        holder.type.setText(post.getType());
        holder.likes_count.setText(String.valueOf(post.getLikes_count()));
        holder.favorites_count.setText(String.valueOf(post.getFavorites_count()));
        holder.comments_count.setText(String.valueOf(post.getComments_count()));
    }

    @Override
    public int getItemCount() {
        return posts.size();
    }

    public static class ViewHolder extends RecyclerView.ViewHolder {
        TextView username;
        TextView post_time;
        TextView content;
        TextView location;
        TextView type;
        TextView likes_count;
        TextView favorites_count;
        TextView comments_count;

        public ViewHolder(View view) {
            super(view);
            username = view.findViewById(R.id.post_username);
            post_time = view.findViewById(R.id.post_time);
            content = view.findViewById(R.id.content);
            location = view.findViewById(R.id.post_location);
            type = view.findViewById(R.id.post_type);
            likes_count = view.findViewById(R.id.likes_count);
            favorites_count = view.findViewById(R.id.favorites_count);
            comments_count = view.findViewById(R.id.comments_count);
        }
    }
}
