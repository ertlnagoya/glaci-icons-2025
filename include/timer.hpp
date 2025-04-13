#pragma once

#include "header.hpp"

#include <chrono>

class AwaitTimer
{
    GLuint query_id;

public:
    AwaitTimer()
    {
        glGenQueries(1, &query_id);
        glBeginQuery(GL_TIME_ELAPSED, query_id);
    };
    ~AwaitTimer() {};

    void begin()
    {
        glBeginQuery(GL_TIME_ELAPSED, query_id);
    };

    void end()
    {
        glEndQuery(GL_TIME_ELAPSED);
    };

    std::chrono::nanoseconds getElapsedTime()
    {
        // Wait until the query result is available
        int done = 0;
        while (!done)
        {
            glGetQueryObjectiv(query_id, GL_QUERY_RESULT_AVAILABLE, &done);
        }

        GLuint64 elapsed_time;
        glGetQueryObjectui64v(query_id, GL_QUERY_RESULT, &elapsed_time);
        return std::chrono::nanoseconds(elapsed_time);
    };
};

class AsyncTimer
{
private:
    static const int BUFFERS = 2;
    // static const int COUNT = 1;
    GLuint query_id[BUFFERS];
    unsigned int backBuffer = 0, frontBuffer = 1;

public:
    AsyncTimer()
    {
        glGenQueries(1, &query_id[backBuffer]);
        glGenQueries(1, &query_id[frontBuffer]);
        glBeginQuery(GL_TIME_ELAPSED, query_id[frontBuffer]);
        glEndQuery(GL_TIME_ELAPSED);
    };
    ~AsyncTimer() {};

    void begin()
    {
        glBeginQuery(GL_TIME_ELAPSED, query_id[backBuffer]);
    };
    void end()
    {
        glEndQuery(GL_TIME_ELAPSED);
        this->_swapBuffer();
    };

    // Return elapsed time in nanoseconds
    std::chrono::nanoseconds getElapsedTime()
    {
        GLuint64 elapsed_time;
        glGetQueryObjectui64v(query_id[frontBuffer], GL_QUERY_RESULT, &elapsed_time);
        return std::chrono::nanoseconds(elapsed_time);
    };

    void _swapBuffer()
    {
        if (backBuffer == 1)
        {
            backBuffer = 0;
            frontBuffer = 1;
        }
        else
        {
            backBuffer = 1;
            frontBuffer = 0;
        }
    };
};
