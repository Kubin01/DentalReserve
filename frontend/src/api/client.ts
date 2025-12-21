import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import { store } from '../store/store';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // 请求拦截器 - 添加token
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // 响应拦截器 - 处理token过期
    this.client.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config;
        
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;
          
          // 尝试刷新token
          try {
            const refreshToken = localStorage.getItem('refresh_token');
            if (!refreshToken) {
              throw new Error('No refresh token');
            }
            
            const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
              refresh_token: refreshToken,
            });
            
            const { access_token } = response.data;
            localStorage.setItem('access_token', access_token);
            
            originalRequest.headers.Authorization = `Bearer ${access_token}`;
            return this.client(originalRequest);
          } catch (refreshError) {
            // 刷新失败，清除本地存储并跳转到登录页
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user');
            window.location.href = '/login';
            return Promise.reject(refreshError);
          }
        }
        
        return Promise.reject(error);
      }
    );
  }

  // 通用请求方法
  async request<T = any>(config: AxiosRequestConfig): Promise<T> {
    try {
      const response: AxiosResponse<T> = await this.client.request(config);
      return response.data;
    } catch (error: any) {
      if (error.response?.data?.detail) {
        throw new Error(error.response.data.detail);
      }
      throw error;
    }
  }

  // GET 请求
  async get<T = any>(url: string, params?: any): Promise<T> {
    return this.request<T>({ method: 'GET', url, params });
  }

  // POST 请求
  async post<T = any>(url: string, data?: any): Promise<T> {
    return this.request<T>({ method: 'POST', url, data });
  }

  // PUT 请求
  async put<T = any>(url: string, data?: any): Promise<T> {
    return this.request<T>({ method: 'PUT', url, data });
  }

  // DELETE 请求
  async delete<T = any>(url: string): Promise<T> {
    return this.request<T>({ method: 'DELETE', url });
  }
}

// 导出单例
export const apiClient = new ApiClient();

// API 端点
export const API_ENDPOINTS = {
  // 认证
  LOGIN: '/auth/token',
  REGISTER: '/auth/register',
  ME: '/auth/me',
  
  // 诊所
  CLINICS: '/clinics',
  CLINIC_DETAIL: (id: string) => `/clinics/${id}`,
  SEARCH_CLINICS: '/clinics/search',
  
  // 医生
  DOCTORS: '/doctors',
  CLINIC_DOCTORS: (clinicId: string) => `/clinics/${clinicId}/doctors`,
  
  // 服务
  SERVICES: '/services',
  CLINIC_SERVICES: (clinicId: string) => `/clinics/${clinicId}/services`,
  
  // 预约
  APPOINTMENTS: '/appointments',
  APPOINTMENT_DETAIL: (id: string) => `/appointments/${id}`,
  AVAILABLE_SLOTS: '/appointments/available-slots',
  CANCEL_APPOINTMENT: (id: string) => `/appointments/${id}/cancel`,
  
  // 电话
  INITIATE_CALL: '/calls/initiate',
  SEND_SMS: '/calls/send-sms',
  
  // 支付
  CREATE_PAYMENT_INTENT: '/payments/create-intent',
  CONFIRM_PAYMENT: '/payments/confirm',
  
  // 评价
  REVIEWS: '/reviews',
  CLINIC_REVIEWS: (clinicId: string) => `/clinics/${clinicId}/reviews`,
};