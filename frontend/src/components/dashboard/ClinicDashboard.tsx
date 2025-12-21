import React, { useState, useEffect } from 'react';
import {
  Calendar,
  Phone,
  Users,
  DollarSign,
  TrendingUp,
  AlertCircle,
  Clock,
  CheckCircle,
  XCircle,
} from 'lucide-react';
import { apiClient, API_ENDPOINTS } from '../../api/client';
import { Appointment, CallLog } from '../../types';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

interface ClinicDashboardProps {
  clinicId: string;
}

const ClinicDashboard: React.FC<ClinicDashboardProps> = ({ clinicId }) => {
  const [dashboardData, setDashboardData] = useState<any>(null);
  const [todayAppointments, setTodayAppointments] = useState<Appointment[]>([]);
  const [recentCalls, setRecentCalls] = useState<CallLog[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
    fetchTodayAppointments();
    fetchRecentCalls();
  }, [clinicId]);

  const fetchDashboardData = async () => {
    try {
      const data = await apiClient.get(`/clinics/${clinicId}/dashboard`);
      setDashboardData(data);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    }
  };

  const fetchTodayAppointments = async () => {
    try {
      const today = new Date().toISOString().split('T')[0];
      const appointments = await apiClient.get('/appointments', {
        clinic_id: clinicId,
        date: today,
      });
      setTodayAppointments(appointments);
    } catch (error) {
      console.error('Failed to fetch today appointments:', error);
    }
  };

  const fetchRecentCalls = async () => {
    try {
      const calls = await apiClient.get('/calls/recent', {
        clinic_id: clinicId,
        limit: 10,
      });
      setRecentCalls(calls);
    } catch (error) {
      console.error('Failed to fetch recent calls:', error);
    }
  };

  // 示例数据
  const appointmentStats = [
    { name: '周一', appointments: 12 },
    { name: '周二', appointments: 19 },
    { name: '周三', appointments: 15 },
    { name: '周四', appointments: 18 },
    { name: '周五', appointments: 14 },
    { name: '周六', appointments: 8 },
    { name: '周日', appointments: 2 },
  ];

  const revenueData = [
    { name: '1月', revenue: 45000 },
    { name: '2月', revenue: 52000 },
    { name: '3月', revenue: 48000 },
    { name: '4月', revenue: 61000 },
    { name: '5月', revenue: 58000 },
    { name: '6月', revenue: 72000 },
  ];

  const serviceDistribution = [
    { name: '洗牙', value: 35 },
    { name: '补牙', value: 25 },
    { name: '根管治疗', value: 15 },
    { name: '牙齿矫正', value: 12 },
    { name: '牙齿美白', value: 8 },
    { name: '其他', value: 5 },
  ];

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D'];

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      {/* Header Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-3 bg-blue-100 rounded-lg mr-4">
              <Calendar className="w-6 h-6 text-blue-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">今日预约</p>
              <p className="text-2xl font-bold">{dashboardData?.today_appointments || 0}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-3 bg-green-100 rounded-lg mr-4">
              <Phone className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">今日通话</p>
              <p className="text-2xl font-bold">{dashboardData?.total_calls || 0}</p>
              <p className="text-sm text-gray-500">
                总时长: {Math.floor((dashboardData?.total_call_duration || 0) / 60)}分钟
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-3 bg-purple-100 rounded-lg mr-4">
              <Users className="w-6 h-6 text-purple-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">新患者</p>
              <p className="text-2xl font-bold">{dashboardData?.new_patients || 0}</p>
              <p className="text-sm text-gray-500">本月新增</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-3 bg-yellow-100 rounded-lg mr-4">
              <DollarSign className="w-6 h-6 text-yellow-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">本月收入</p>
              <p className="text-2xl font-bold">${dashboardData?.monthly_revenue?.toFixed(2) || '0.00'}</p>
              <div className="flex items-center text-sm">
                <TrendingUp className="w-4 h-4 text-green-500 mr-1" />
                <span className="text-green-500">+12.5%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* 预约趋势 */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4">每周预约趋势</h3>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={appointmentStats}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="appointments"
                  stroke="#0088FE"
                  strokeWidth={2}
                  dot={{ strokeWidth: 2 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* 收入趋势 */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4">月度收入趋势</h3>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={revenueData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip formatter={(value) => [`$${value}`, '收入']} />
                <Legend />
                <Bar dataKey="revenue" fill="#00C49F" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Bottom Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* 今日预约 */}
        <div className="bg-white rounded-lg shadow lg:col-span-2">
          <div className="p-6 border-b border-gray-200">
            <h3 className="text-lg font-semibold">今日预约</h3>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    时间
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    患者
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    服务
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    医生
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    状态
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    操作
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {todayAppointments.map((appointment) => (
                  <tr key={appointment.id}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <Clock className="w-4 h-4 mr-2 text-gray-400" />
                        {appointment.start_time}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <Users className="w-4 h-4 mr-2 text-gray-400" />
                        {appointment.patient?.first_name} {appointment.patient?.last_name}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {appointment.service?.name}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {appointment.doctor?.name || '未指定'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        appointment.status === 'confirmed'
                          ? 'bg-green-100 text-green-800'
                          : appointment.status === 'pending'
                          ? 'bg-yellow-100 text-yellow-800'
                          : 'bg-red-100 text-red-800'
                      }`}>
                        {appointment.status === 'confirmed' ? (
                          <CheckCircle className="w-3 h-3 mr-1" />
                        ) : (
                          <XCircle className="w-3 h-3 mr-1" />
                        )}
                        {appointment.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <button className="text-blue-600 hover:text-blue-900 mr-3">
                        查看
                      </button>
                      <button className="text-green-600 hover:text-green-900">
                        致电
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* 服务分布 */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b border-gray-200">
            <h3 className="text-lg font-semibold">服务项目分布</h3>
          </div>
          <div className="p-6">
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={serviceDistribution}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {serviceDistribution.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value) => [`${value}%`, '占比']} />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ClinicDashboard;